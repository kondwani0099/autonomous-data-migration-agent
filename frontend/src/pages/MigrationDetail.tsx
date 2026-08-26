import React, { useEffect, useState } from 'react';
import { MigrationJob, DataPreview, AuditLogEntry, DocumentItem } from '../types';
import { api } from '../services/api';
import { MigrationProgress } from '../components/MigrationProgress';
import { DataPreviewTable } from '../components/DataPreviewTable';
import { AgentLog } from '../components/AgentLog';
import { FileText, CheckCircle2, XCircle, Loader2 } from 'lucide-react';

const CATEGORY_LABELS: Record<string, string> = {
  sales: 'Sales',
  expenses: 'Expenses',
  payroll: 'Payroll',
  invoices: 'Invoices',
  purchases: 'Purchases',
  other: 'Other',
};

interface MigrationDetailProps {
  jobId: string;
  onNavigate: (page: string) => void;
}

export const MigrationDetail: React.FC<MigrationDetailProps> = ({ jobId, onNavigate }) => {
  const [job, setJob] = useState<MigrationJob | null>(null);
  const [preview, setPreview] = useState<DataPreview | null>(null);
  const [auditEntries, setAuditEntries] = useState<AuditLogEntry[]>([]);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);

  useEffect(() => {
    api.getJob(jobId).then(setJob).catch(() => {});
    api.getPreview(jobId).then(setPreview).catch(() => {});
    api.getAuditTrail(jobId).then(setAuditEntries).catch(() => {});
    api.getDocuments(jobId).then(setDocuments).catch(() => {});
  }, [jobId]);

  const handleApprove = async () => {
    await api.approveImport(jobId);
    if (job) {
      setJob({ ...job, status: 'completed' });
    }
  };

  if (!job) {
    return <div className="text-center text-xs text-slate-400 dark:text-slate-500 py-12">Loading job details...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <button onClick={() => onNavigate('dashboard')} className="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 mb-2">
            &larr; Back to Dashboard
          </button>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100">{job.client_name}</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">Job ID: {job.job_id}</p>
        </div>
        <div className="flex flex-col items-end space-y-2">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
            {CATEGORY_LABELS[job.data_category] || job.data_category} Data
          </span>
        </div>
      </div>

      <MigrationProgress status={job.status} />

      {documents.length > 0 && (
        <div className="glass-card p-6 space-y-4">
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200 flex items-center space-x-2">
            <FileText className="w-4 h-4 text-indigo-500 dark:text-indigo-400" />
            <span>Uploaded Documents ({documents.length})</span>
          </h3>
          <div className="space-y-2">
            {documents.map((doc) => (
              <div
                key={doc.document_id}
                className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800"
              >
                <div className="min-w-0">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-medium text-slate-800 dark:text-slate-200 truncate">{doc.file_name}</span>
                    {doc.status === 'completed' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                    ) : doc.status === 'failed' ? (
                      <XCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                    ) : (
                      <Loader2 className="w-4 h-4 text-amber-500 animate-spin flex-shrink-0" />
                    )}
                  </div>
                  {doc.extracted_columns.length > 0 && (
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1 font-mono truncate">
                      {doc.extracted_columns.join(', ')}
                    </p>
                  )}
                </div>
                <span className={`text-[11px] px-2.5 py-1 rounded-full font-semibold flex-shrink-0 ${
                  doc.status === 'completed'
                    ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                    : doc.status === 'failed'
                    ? 'bg-red-500/10 text-red-600 dark:text-red-400'
                    : 'bg-amber-500/10 text-amber-600 dark:text-amber-400'
                }`}>
                  {doc.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {preview && (
        <DataPreviewTable
          preview={preview}
          onApprove={handleApprove}
          onUpdated={(updated) => setPreview(updated)}
        />
      )}

      <AgentLog entries={auditEntries} />
    </div>
  );
};
