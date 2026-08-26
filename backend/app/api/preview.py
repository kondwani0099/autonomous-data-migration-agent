"""Preview, approval, and audit endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.models.schemas import DataPreview, JobStatus, EditableRecordsRequest
from app.services.firestore import firestore_service

router = APIRouter()


@router.get("/{job_id}/preview", response_model=DataPreview)
async def get_job_preview(job_id: str) -> DataPreview:
    job = await firestore_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    preview_data = await firestore_service.get_preview(job_id)
    audit = await firestore_service.get_audit_trail(job_id)

    if preview_data:
        return DataPreview(**preview_data)

    # Fallback: return empty preview if no data processed yet
    return DataPreview(
        job_id=job_id,
        total_records=0,
        clean_count=0,
        anomalies=[],
        sample_records=[],
        audit_trail=audit,
    )


@router.post("/{job_id}/preview", response_model=DataPreview)
async def save_edited_records(job_id: str, payload: EditableRecordsRequest) -> DataPreview:
    """Persist user-edited records (Excel-like editing) back to the job preview."""
    job = await firestore_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    preview_data = await firestore_service.get_preview(job_id) or {}

    edited = payload.records
    preview_data["records"] = edited
    preview_data["sample_records"] = edited[:50]
    preview_data["total_records"] = len(edited)
    preview_data["clean_count"] = len(edited) - len(preview_data.get("anomalies", []))

    await firestore_service.save_preview(job_id, preview_data)

    from app.models.schemas import AuditLogEntry

    entry = AuditLogEntry(
        agent="HumanReview",
        action="Edited records in preview",
        details=f"User edited/confirmed {len(edited)} records in the preview grid",
        after={"total_records": len(edited)},
    )
    await firestore_service.add_audit_entry(job_id, entry.model_dump())

    return DataPreview(**preview_data)


@router.post("/{job_id}/approve")
async def approve_job_import(job_id: str) -> dict:
    job = await firestore_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Import count comes from the (possibly user-edited) preview records
    imported_records = 0
    preview_data = await firestore_service.get_preview(job_id)
    if preview_data:
        imported_records = len(preview_data.get("records", []))

    # Mark job completed and record imported count
    job.status = JobStatus.COMPLETED
    job.records_imported = imported_records
    await firestore_service.update_job(job)

    return {
        "status": "success",
        "job_id": job_id,
        "imported_records": imported_records,
    }

@router.get("/{job_id}/audit")
async def get_job_audit(job_id: str) -> List[Dict[str, Any]]:
    return await firestore_service.get_audit_trail(job_id)
