import React, { useEffect, useState } from 'react';
import { MigrationJob, Clarification, DataPreview } from '../types';
import { api } from '../services/api';
import { MigrationProgress } from '../components/MigrationProgress';
import { ClarificationCard } from '../components/ClarificationCard';
import { DataPreviewTable } from '../components/DataPreviewTable';
import { AgentLog } from '../components/AgentLog';

interface MigrationDetailProps {
  jobId: string;
  onNavigate: (page: string) => void;
}

export const MigrationDetail: React.FC<MigrationDetailProps> = ({ jobId, onNavigate }) => {
  const [job, setJob] = useState<MigrationJob | null>(null);
  const [clarifications, setClarifications] = useState<Clarification[]>([]);
  const [preview, setPreview] = useState<DataPreview | null>(null);

  useEffect(() => {
    api.getJob(jobId).then(setJob).catch(() => {});
    api.getClarifications(jobId).then(setClarifications).catch(() => {});
    api.getPreview(jobId).then(setPreview).catch(() => {});
  }, [jobId]);

  const handleAnswerSubmit = async (clarificationId: string, answer: string) => {
    await api.answerClarification(clarificationId, answer);
    setClarifications((prev) => prev.filter((c) => c.clarification_id !== clarificationId));
  };

  const handleApprove = async () => {
    await api.approveImport(jobId);
    if (job) {
      setJob({ ...job, status: 'completed' });
    }
  };

  if (!job) {
    return <div className="text-center text-xs text-slate-500 py-12">Loading job details...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <button onClick={() => onNavigate('dashboard')} className="text-xs text-slate-400 hover:text-slate-200 mb-2">
            &larr; Back to Dashboard
          </button>
          <h1 className="text-2xl font-bold text-slate-100">{job.client_name}</h1>
          <p className="text-xs text-slate-400 font-mono">Job ID: {job.job_id}</p>
        </div>
      </div>

      <MigrationProgress status={job.status} />

      {clarifications.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-amber-400 uppercase tracking-wider">
            Pending Agent Questions ({clarifications.length})
          </h3>
          {clarifications.map((clar) => (
            <ClarificationCard
              key={clar.clarification_id}
              clarification={clar}
              onAnswerSubmit={handleAnswerSubmit}
            />
          ))}
        </div>
      )}

      {preview && <DataPreviewTable preview={preview} onApprove={handleApprove} />}

      <AgentLog entries={[]} />
    </div>
  );
};
