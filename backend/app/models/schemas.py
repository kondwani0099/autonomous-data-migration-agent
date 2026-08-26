"""Pydantic v2 domain schemas for Migration Jobs, Documents, and Agent Data structures."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class JobStatus(str, Enum):
    UPLOADING = "uploading"
    UNDERSTANDING = "understanding"
    MAPPING = "mapping"
    CLEANING = "cleaning"
    CLARIFYING = "clarifying"
    AWAITING_APPROVAL = "awaiting_approval"
    IMPORTING = "importing"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentType(str, Enum):
    SALES_LEDGER = "SALES_LEDGER"
    INVENTORY_SHEET = "INVENTORY_SHEET"
    PURCHASE_RECORD = "PURCHASE_RECORD"
    PATIENT_RECORD = "PATIENT_RECORD"
    INVOICE = "INVOICE"
    UNKNOWN = "UNKNOWN"


class DataCategory(str, Enum):
    """Target ERP data format the migration agents will normalize records into."""

    SALES = "sales"
    EXPENSES = "expenses"
    PAYROLL = "payroll"
    INVOICES = "invoices"
    PURCHASES = "purchases"
    OTHER = "other"


class ClarificationStatus(str, Enum):
    PENDING = "pending"
    ANSWERED = "answered"
    APPLIED = "applied"

class CreateJobRequest(BaseModel):
    client_id: str
    client_name: str
    description: Optional[str] = None
    data_category: DataCategory = DataCategory.SALES

class DocumentItem(BaseModel):
    document_id: str
    job_id: str
    file_name: str
    file_path: str
    file_type: str
    status: str = "queued"
    document_type: DocumentType = DocumentType.UNKNOWN
    extracted_columns: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class MigrationJob(BaseModel):
    job_id: str
    client_id: str
    client_name: str
    status: JobStatus = JobStatus.UPLOADING
    data_category: DataCategory = DataCategory.SALES
    total_documents: int = 0
    processed_documents: int = 0
    total_records_detected: int = 0
    records_imported: int = 0
    anomalies_found: int = 0
    clarifications_pending: int = 0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ClarificationRequest(BaseModel):
    clarification_id: str
    job_id: str
    document_id: str
    agent: str
    question: str
    options: List[str]
    context: str
    status: ClarificationStatus = ClarificationStatus.PENDING
    answer: Optional[str] = None

class ClarificationAnswer(BaseModel):
    answer: str

class DataAnomaly(BaseModel):
    record_index: int
    field: str
    reason: str
    severity: str = "warning"  # warning, error
    value: Any

class AuditLogEntry(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    agent: str
    action: str
    document_id: Optional[str] = None
    details: str
    before: Optional[Any] = None
    after: Optional[Any] = None

class DataPreview(BaseModel):
    job_id: str
    total_records: int
    clean_count: int
    anomalies: List[DataAnomaly] = Field(default_factory=list)
    sample_records: List[Dict[str, Any]] = Field(default_factory=list)
    audit_trail: List[AuditLogEntry] = Field(default_factory=list)
    target_schema: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {"label": "Sales", "columns": []}
    )
    # Full editable record set (Excel-like editing in the frontend)
    records: List[Dict[str, Any]] = Field(default_factory=list)
    # Per-document column mappings produced by the SchemaMappingAgent
    mappings: List[Dict[str, Any]] = Field(default_factory=list)


class EditableRecordsRequest(BaseModel):
    """Payload for saving user-edited records back to a job preview."""

    records: List[Dict[str, Any]] = Field(default_factory=list)

class ClientMapping(BaseModel):
    client_id: str
    mappings: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    product_normalizations: Dict[str, List[str]] = Field(default_factory=dict)
