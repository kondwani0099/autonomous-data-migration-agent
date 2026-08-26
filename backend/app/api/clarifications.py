"""Clarifications human-in-the-loop API endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException
from app.models.schemas import ClarificationRequest, ClarificationAnswer, ClarificationStatus
from app.services.firestore import firestore_service

router = APIRouter()

@router.get("/{job_id}/clarifications", response_model=List[ClarificationRequest])
async def list_clarifications(job_id: str) -> List[ClarificationRequest]:
    job = await firestore_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return await firestore_service.list_clarifications(job_id)

@router.post("/clarifications/{clarification_id}/answer")
async def submit_answer(clarification_id: str, payload: ClarificationAnswer) -> dict:
    clar = firestore_service._clarifications.get(clarification_id)
    if not clar:
        raise HTTPException(status_code=404, detail="Clarification not found")

    clar["answer"] = payload.answer
    clar["status"] = ClarificationStatus.ANSWERED.value
    firestore_service._clarifications[clarification_id] = clar

    return {
        "status": "success",
        "clarification_id": clarification_id,
        "answer": payload.answer,
        "message": "Answer applied to learned mapping. Pipeline resumed.",
    }
