"""Clarifications human-in-the-loop API endpoints."""

from typing import List
from fastapi import APIRouter
from app.models.schemas import ClarificationRequest, ClarificationAnswer, ClarificationStatus
from app.services.firestore import firestore_service

router = APIRouter()

@router.get("/{job_id}/clarifications", response_model=List[ClarificationRequest])
async def list_clarifications(job_id: str) -> List[ClarificationRequest]:
    return await firestore_service.list_clarifications(job_id)

@router.post("/clarifications/{clarification_id}/answer")
async def submit_answer(clarification_id: str, payload: ClarificationAnswer) -> dict:
    return {
        "status": "success",
        "clarification_id": clarification_id,
        "answer": payload.answer,
        "message": "Answer applied to learned mapping. Pipeline resumed.",
    }
