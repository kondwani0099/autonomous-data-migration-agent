import React from 'react';
import { JobStatus } from '../types';
import { CheckCircle2, Clock, HelpCircle, Loader2 } from 'lucide-react';

interface MigrationProgressProps {
  status: JobStatus;
}

const STAGES: { id: JobStatus; label: string }[] = [
  { id: 'uploading', label: '1. Ingest' },
  { id: 'understanding', label: '2. Understand' },
  { id: 'mapping', label: '3. Schema Map' },
  { id: 'cleaning', label: '4. Clean & Normalize' },
  { id: 'awaiting_approval', label: '5. Dry-Run Preview' },
  { id: 'completed', label: '6. Imported' },
];

export const MigrationProgress: React.FC<MigrationProgressProps> = ({ status }) => {
  const getStageIndex = (s: JobStatus) => {
    switch (s) {
      case 'uploading': return 0;
      case 'understanding': return 1;
      case 'mapping': return 2;
      case 'clarifying': return 2;
      case 'cleaning': return 3;
      case 'awaiting_approval': return 4;
      case 'importing': return 5;
      case 'completed': return 5;
      default: return 0;
    }
  };

  const currentIndex = getStageIndex(status);

  return (
    <div className="w-full glass-card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300">Agent Swarm Pipeline Progress</h3>
        <span className="text-xs font-mono px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
          Status: {status.toUpperCase()}
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
        {STAGES.map((stage, idx) => {
          const isDone = idx < currentIndex || status === 'completed';
          const isCurrent = idx === currentIndex && status !== 'completed';

          return (
            <div
              key={stage.id}
              className={`p-3 rounded-xl border transition-all duration-300 flex flex-col items-center justify-center text-center ${
                isDone
                  ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-500/30 text-emerald-600 dark:text-emerald-300'
                  : isCurrent
                  ? 'bg-indigo-50 dark:bg-indigo-950/40 border-indigo-400 dark:border-indigo-500/50 text-indigo-600 dark:text-indigo-200 ring-2 ring-indigo-500/20'
                  : 'bg-slate-50 dark:bg-slate-900/40 border-slate-200 dark:border-slate-800/80 text-slate-400 dark:text-slate-500'
              }`}
            >
              <div className="mb-2">
                {isDone ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 dark:text-emerald-400" />
                ) : isCurrent ? (
                  status === 'clarifying' ? (
                    <HelpCircle className="w-5 h-5 text-amber-500 dark:text-amber-400 animate-pulse" />
                  ) : (
                    <Loader2 className="w-5 h-5 text-indigo-500 dark:text-indigo-400 animate-spin" />
                  )
                ) : (
                  <Clock className="w-5 h-5 text-slate-400 dark:text-slate-600" />
                )}
              </div>
              <span className="text-xs font-medium">{stage.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
