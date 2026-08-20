export type JobStatus =
  | 'uploading'
  | 'understanding'
  | 'mapping'
  | 'cleaning'
  | 'clarifying'
  | 'awaiting_approval'
  | 'importing'
  | 'completed'
  | 'failed';

export interface MigrationJob {
  job_id: string;
  client_id: string;
  client_name: string;
  status: JobStatus;
  total_documents: number;
  processed_documents: number;
  total_records_detected: number;
  records_imported: number;
  anomalies_found: number;
  clarifications_pending: number;
  created_at: string;
  updated_at: string;
}

export interface DocumentItem {
  document_id: string;
  job_id: string;
  file_name: string;
  file_path: string;
  file_type: string;
  status: string;
  document_type: string;
  extracted_columns: string[];
  confidence_score: number;
  created_at: string;
}

export interface Clarification {
  clarification_id: string;
  job_id: string;
  document_id: string;
  agent: string;
  question: string;
  options: string[];
  context: string;
  status: 'pending' | 'answered' | 'applied';
  answer?: string;
}

export interface DataAnomaly {
  record_index: number;
  field: string;
  reason: string;
  severity: 'warning' | 'error';
  value: unknown;
}

export interface AuditLogEntry {
  timestamp: string;
  agent: string;
  action: string;
  document_id?: string;
  details: string;
  before?: unknown;
  after?: unknown;
}

export interface DataPreview {
  job_id: string;
  total_records: number;
  clean_count: number;
  anomalies: DataAnomaly[];
  sample_records: Record<string, unknown>[];
  audit_trail: AuditLogEntry[];
}
