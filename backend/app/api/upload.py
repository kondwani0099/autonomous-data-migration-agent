"""Upload & GCS signed URL generation endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.storage import storage_service

router = APIRouter()

class UploadUrlRequest(BaseModel):
    file_name: str

class UploadUrlResponse(BaseModel):
    upload_url: str
    file_path: str

@router.post("/{job_id}/upload-url", response_model=UploadUrlResponse)
async def get_upload_url(job_id: str, payload: UploadUrlRequest) -> UploadUrlResponse:
    url = storage_service.generate_upload_url(job_id, payload.file_name)
    return UploadUrlResponse(
        upload_url=url,
        file_path=f"gs://uniplexity-migration-uploads/jobs/{job_id}/{payload.file_name}",
    )
