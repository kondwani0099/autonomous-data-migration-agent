"""Preview, approval, and audit endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter
from app.models.schemas import DataPreview, JobStatus
from app.services.firestore import firestore_service

router = APIRouter()

@router.get("/{job_id}/preview", response_model=DataPreview)
async def get_job_preview(job_id: str) -> DataPreview:
    audit = await firestore_service.get_audit_trail(job_id)
    return DataPreview(
        job_id=job_id,
        total_records=2847,
        clean_count=2835,
        anomalies=[],
        sample_records=[
            {"sale_date": "2024-01-15", "customer_name": "ABC Retail Store", "product_name": "Coca-Cola", "quantity": 10, "unit_price": 1.50, "total_amount": 15.00},
            {"sale_date": "2024-01-16", "customer_name": "XYZ Market", "product_name": "Sliced Bread", "quantity": 20, "unit_price": 2.00, "total_amount": 40.00},
        ],
        audit_trail=[],
    )

@router.post("/{job_id}/approve")
async def approve_job_import(job_id: str) -> dict:
    await firestore_service.update_job_status(job_id, JobStatus.COMPLETED)
    return {"status": "success", "job_id": job_id, "imported_records": 2835}

@router.get("/{job_id}/audit")
async def get_job_audit(job_id: str) -> List[Dict[str, Any]]:
    return await firestore_service.get_audit_trail(job_id)
