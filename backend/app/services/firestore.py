"""Firestore state persistence service layer with in-memory fallback for local development."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.schemas import MigrationJob, DocumentItem, ClarificationRequest, JobStatus, DataPreview

class FirestoreService:
    def __init__(self) -> None:
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._clarifications: Dict[str, Dict[str, Any]] = {}
        self._client_mappings: Dict[str, Dict[str, Any]] = {}
        self._audit_trails: Dict[str, List[Dict[str, Any]]] = {}
        self._previews: Dict[str, Dict[str, Any]] = {}

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

    async def update_job(self, job: MigrationJob) -> MigrationJob:
        """Update an existing job with new data."""
        self._jobs[job.job_id] = job.model_dump()
        return job

    async def create_document(self, doc: DocumentItem) -> DocumentItem:
        """Create a new document record (alias for add_document)."""
        return await self.add_document(doc)

    async def update_document(self, doc: DocumentItem) -> DocumentItem:
        """Update an existing document."""
        self._documents[doc.document_id] = doc.model_dump()
        return doc

    async def get_document(self, document_id: str) -> Optional[DocumentItem]:
        """Get a document by ID."""
        data = self._documents.get(document_id)
        if data:
            return DocumentItem(**data)
        return None

    async def create_clarifications(
        self, clarifications: List[Dict[str, Any]], job_id: str, document_id: str
    ) -> List[ClarificationRequest]:
        """Create multiple clarification requests."""
        import uuid
        created: List[ClarificationRequest] = []
        for c in clarifications:
            clar_id = f"clar_{uuid.uuid4().hex[:8]}"
            clar = ClarificationRequest(
                clarification_id=clar_id,
                job_id=job_id,
                document_id=document_id,
                agent=c.get("agent", "SchemaMappingAgent"),
                question=c.get("question", ""),
                options=c.get("options", []),
                context=c.get("context", ""),
            )
            await self.add_clarification(clar)
            created.append(clar)
        return created

    async def save_preview(self, job_id: str, preview: Dict[str, Any]) -> None:
        """Save preview data for a job."""
        self._previews[job_id] = preview

    async def get_preview(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get preview data for a job."""
        return self._previews.get(job_id)

firestore_service = FirestoreService()
