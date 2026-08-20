"""Migration Jobs API endpoints."""

import uuid
from typing import List
from fastapi import APIRouter, HTTPException
from app.models.schemas import MigrationJob, CreateJobRequest, JobStatus
from app.services.firestore import firestore_service

router = APIRouter()

@router.post("", response_model=MigrationJob)
async def create_job(payload: CreateJobRequest) -> MigrationJob:
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    job = MigrationJob(
        job_id=job_id,
        client_id=payload.client_id,
        client_name=payload.client_name,
        status=JobStatus.UPLOADING,
    )
    return await firestore_service.create_job(job)

@router.get("", response_model=List[MigrationJob])
async def list_jobs() -> List[MigrationJob]:
    return await firestore_service.list_jobs()

@router.get("/{job_id}", response_model=MigrationJob)
async def get_job(job_id: str) -> MigrationJob:
    job = await firestore_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
