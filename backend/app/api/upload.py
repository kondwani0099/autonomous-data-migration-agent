"""Upload & file processing endpoints."""

import asyncio
import os
import uuid
from typing import Any, Dict, List, Tuple

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.agents.pipeline import migration_pipeline
from app.services.firestore import firestore_service
from app.services.storage import storage_service
from app.models.schemas import DocumentItem, JobStatus

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")


class UploadUrlRequest(BaseModel):
    file_name: str


class UploadUrlResponse(BaseModel):
    upload_url: str
    file_path: str


class FileUploadResponse(BaseModel):
    document_id: str
    file_name: str
    file_type: str
    status: str
    message: str


@router.post("/{job_id}/upload-url", response_model=UploadUrlResponse)
async def get_upload_url(job_id: str, payload: UploadUrlRequest) -> UploadUrlResponse:
    url = storage_service.generate_upload_url(job_id, payload.file_name)
    return UploadUrlResponse(
        upload_url=url,
        file_path=f"gs://uniplexity-migration-uploads/jobs/{job_id}/{payload.file_name}",
    )


@router.post("/{job_id}/upload", response_model=List[FileUploadResponse])
async def upload_file(
    job_id: str,
    files: List[UploadFile] = File(...),
) -> List[FileUploadResponse]:
    """Upload one or more files for a migration job and process them concurrently.

    Each document runs through the full agent pipeline (extract -> map -> clean).
    Clean records from all documents are aggregated into a single dry-run preview.
    """
    # Verify job exists
    job = await firestore_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    data_category = job.data_category.value if job.data_category else "sales"

    # Create upload directory
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_DIR, job_id), exist_ok=True)

    supported = {"csv", "xlsx", "xls", "pdf", "png", "jpg", "jpeg"}
    prepared: List[Dict[str, Any]] = []

    # Save all files & create document records first
    for file in files:
        if not file.filename:
            continue

        file_ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if file_ext not in supported:
            raise HTTPException(
                status_code=400,
                detail=f"File type .{file_ext} is not supported. Supported: {', '.join(sorted(supported))}",
            )

        file_id = uuid.uuid4().hex[:8]
        file_path = os.path.join(UPLOAD_DIR, job_id, f"{file_id}.{file_ext}")
        file_data = await file.read()
        with open(file_path, "wb") as f:
            f.write(file_data)

        document_id = f"doc_{file_id}"
        doc = DocumentItem(
            document_id=document_id,
            job_id=job_id,
            file_name=file.filename,
            file_path=file_path,
            file_type=file_ext,
            status="processing",
        )
        await firestore_service.create_document(doc)
        prepared.append({
            "doc": doc,
            "file_path": file_path,
            "file_ext": file_ext,
            "file_data": file_data,
        })

    # Process all documents concurrently through the agent pipeline
    async def _process_one(item: Dict[str, Any]) -> Tuple[FileUploadResponse, Dict[str, Any] | None]:
        doc = item["doc"]
        error_message = ""
        result: Dict[str, Any] | None = None
        try:
            result = await _process_document(
                job_id, doc.document_id, item["file_path"], item["file_ext"], item["file_data"], data_category
            )
            # Re-fetch the doc so per-document fields (extracted_columns, confidence) set
            # during processing are preserved when we mark it completed.
            fresh_doc = await firestore_service.get_document(doc.document_id)
            if fresh_doc:
                doc = fresh_doc
            doc.status = "completed"
        except Exception as e:
            doc.status = "failed"
            error_message = str(e)
            print(f"Error processing {doc.file_name}: {e}")

        await firestore_service.update_document(doc)
        response = FileUploadResponse(
            document_id=doc.document_id,
            file_name=doc.file_name,
            file_type=doc.file_type,
            status=doc.status,
            message=(
                f"File {doc.file_name} processed successfully"
                if doc.status == "completed"
                else f"File {doc.file_name} failed: {error_message}"
            ),
        )
        return response, result

    outcomes = await asyncio.gather(*(_process_one(item) for item in prepared))
    results: List[FileUploadResponse] = [outcome[0] for outcome in outcomes]

    # Aggregate clean records + anomalies + per-document mappings across all docs
    all_clean: List[Dict[str, Any]] = []
    all_anomalies: List[Dict[str, Any]] = []
    all_mappings: List[Dict[str, Any]] = []
    for _, result in outcomes:
        if result:
            all_clean.extend(result.get("clean_records", []))
            all_anomalies.extend(result.get("anomalies", []))
            if result.get("mappings"):
                all_mappings.append({
                    "document_id": result.get("document_id", ""),
                    "file_name": result.get("file_name", ""),
                    "mappings": result.get("mappings"),
                })

    await _aggregate_preview(job_id, data_category, all_clean, all_anomalies, all_mappings)

    # Update job counters & final status
    fresh_job = await firestore_service.get_job(job_id)
    if fresh_job:
        fresh_job.total_documents = len(results)
        fresh_job.processed_documents = sum(1 for r in results if r.status == "completed")
        fresh_job.total_records_detected = sum(
            result.get("raw_count", 0) for _, result in outcomes if result
        )
        fresh_job.anomalies_found = len(all_anomalies)
        fresh_job.clarifications_pending = len(
            await firestore_service.list_clarifications(job_id)
        )
        fresh_job.status = JobStatus.AWAITING_APPROVAL
        fresh_job.records_imported = 0
        await firestore_service.update_job(fresh_job)

    return results


async def _aggregate_preview(
    job_id: str,
    data_category: str,
    clean_records: List[Dict[str, Any]],
    anomalies: List[Dict[str, Any]],
    mappings: List[Dict[str, Any]] | None = None,
) -> None:
    """Combine clean records + anomalies + mappings from all documents into one saved preview."""
    from app.agents.tools import get_category_schema
    from app.models.schemas import DataAnomaly

    target_schema = get_category_schema(data_category)
    if not clean_records:
        empty = await migration_pipeline.validation_agent.generate_preview(
            job_id, [], [], target_schema, mappings or []
        )
        await firestore_service.save_preview(job_id, empty.model_dump())
        return

    anomaly_models = [DataAnomaly(**a) if isinstance(a, dict) else a for a in anomalies]
    preview = await migration_pipeline.validation_agent.generate_preview(
        job_id, clean_records, anomaly_models, target_schema, mappings or []
    )
    await firestore_service.save_preview(job_id, preview.model_dump())

    await _log_agent_step(
        job_id, "", "ValidationImportAgent", "Generated dry-run preview",
        f"Preview ready: {len(clean_records)} clean records aggregated from multiple documents",
        after={"total_records": len(clean_records), "anomalies": len(anomalies)},
    )


async def _process_document(
    job_id: str,
    document_id: str,
    file_path: str,
    file_ext: str,
    file_data: bytes,
    data_category: str = "sales",
) -> Dict[str, Any]:
    """Run a single document through the agent pipeline and return processed data.

    Returns a dict with ``columns``, ``raw_records``, ``clean_records``, ``anomalies``
    and counts. The caller is responsible for aggregating & saving the final preview.
    """
    from app.services.document_parser import document_parser

    # Step 1: Parse document
    parse_result = await document_parser.parse_document_async(file_data, file_ext)

    if parse_result.get("error"):
        raise ValueError(f"Document parsing failed: {parse_result['error']}")

    columns = parse_result.get("detected_columns", [])
    raw_records = parse_result.get("raw_records", [])
    confidence = parse_result.get("confidence_score", 0.0)

    # Update document with extracted columns
    doc = await firestore_service.get_document(document_id)
    if doc:
        doc.extracted_columns = columns
        doc.confidence_score = confidence
        await firestore_service.update_document(doc)

    await _log_agent_step(
        job_id, document_id, "DocumentUnderstandingAgent", "Extracted document data",
        f"Extracted {len(raw_records)} records from {file_ext.upper()} document with {len(columns)} columns (confidence {confidence:.0%})",
        after={"detected_columns": columns, "total_records": len(raw_records)},
    )

    if not raw_records:
        raise ValueError("No records could be extracted from the document")

    # Step 2: Schema mapping (AI-driven when a real API key is available)
    job = await firestore_service.get_job(job_id)
    mappings, clarifications = await migration_pipeline.schema_agent.map_columns(
        job.client_id if job else "unknown", columns, data_category
    )

    await _log_agent_step(
        job_id, document_id, "SchemaMappingAgent", "Mapped raw columns to Uniplexity ERP schema",
        f"Detected {len(columns)} columns -> {len(mappings)} mappings for '{data_category}' format; {len(clarifications) if clarifications else 0} clarifications raised",
        before={"detected_columns": columns},
        after={"mappings": mappings, "data_category": data_category},
    )

    if clarifications:
        await firestore_service.create_clarifications(clarifications, job_id, document_id)

    # Step 3: Data cleaning
    clean_records, anomalies = await migration_pipeline.cleaning_agent.clean_and_normalize(
        raw_records, mappings, data_category
    )

    await _log_agent_step(
        job_id, document_id, "DataCleaningAgent", "Cleaned and normalized records",
        f"Normalized {len(clean_records)} records; flagged {len(anomalies)} anomalies",
        before={"raw_records": len(raw_records)},
        after={"clean_records": len(clean_records), "anomalies": len(anomalies)},
    )

    return {
        "document_id": document_id,
        "file_name": file_path.rsplit(os.sep, 1)[-1],
        "columns": columns,
        "mappings": mappings,
        "raw_records": raw_records,
        "clean_records": clean_records,
        "anomalies": anomalies,
        "raw_count": len(raw_records),
        "clean_count": len(clean_records),
    }


async def _log_agent_step(
    job_id: str,
    document_id: str,
    agent: str,
    action: str,
    details: str,
    before: Dict[str, Any] | None = None,
    after: Dict[str, Any] | None = None,
) -> None:
    """Write an audit trail entry for an agent pipeline step."""
    from app.models.schemas import AuditLogEntry

    entry = AuditLogEntry(
        agent=agent,
        action=action,
        document_id=document_id,
        details=details,
        before=before,
        after=after,
    )
    await firestore_service.add_audit_entry(job_id, entry.model_dump())
