"""Firestore state persistence service layer with in-memory fallback for local development."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.schemas import MigrationJob, DocumentItem, ClarificationRequest, JobStatus

class FirestoreService:
    def __init__(self) -> None:
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._clarifications: Dict[str, Dict[str, Any]] = {}
        self._client_mappings: Dict[str, Dict[str, Any]] = {}
        self._audit_trails: Dict[str, List[Dict[str, Any]]] = {}

    async def create_job(self, job: MigrationJob) -> MigrationJob:
        self._jobs[job.job_id] = job.model_dump()
        return job

    async def get_job(self, job_id: str) -> Optional[MigrationJob]:
        data = self._jobs.get(job_id)
        if data:
            return MigrationJob(**data)
        return None

    async def list_jobs(self) -> List[MigrationJob]:
        return [MigrationJob(**job) for job in self._jobs.values()]

    async def update_job_status(self, job_id: str, status: JobStatus) -> Optional[MigrationJob]:
        if job_id in self._jobs:
            self._jobs[job_id]["status"] = status.value
            self._jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
            return MigrationJob(**self._jobs[job_id])
        return None

    async def add_document(self, doc: DocumentItem) -> DocumentItem:
        self._documents[doc.document_id] = doc.model_dump()
        return doc

    async def list_documents(self, job_id: str) -> List[DocumentItem]:
        return [
            DocumentItem(**doc)
            for doc in self._documents.values()
            if doc["job_id"] == job_id
        ]

    async def add_clarification(self, clar: ClarificationRequest) -> ClarificationRequest:
        self._clarifications[clar.clarification_id] = clar.model_dump()
        return clar

    async def list_clarifications(self, job_id: str) -> List[ClarificationRequest]:
        return [
            ClarificationRequest(**c)
            for c in self._clarifications.values()
            if c["job_id"] == job_id
        ]

    async def add_audit_entry(self, job_id: str, entry: Dict[str, Any]) -> None:
        if job_id not in self._audit_trails:
            self._audit_trails[job_id] = []
        self._audit_trails[job_id].append(entry)

    async def get_audit_trail(self, job_id: str) -> List[Dict[str, Any]]:
        return self._audit_trails.get(job_id, [])

firestore_service = FirestoreService()
