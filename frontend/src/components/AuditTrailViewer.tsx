import React from 'react';
import { AuditLogEntry } from '../types';
import { ShieldCheck, FileSpreadsheet } from 'lucide-react';

interface AuditTrailViewerProps {
  logs: AuditLogEntry[];
}

export const AuditTrailViewer: React.FC<AuditTrailViewerProps> = ({ logs }) => {
  return (
    <div className="glass-card p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-semibold text-slate-800 dark:text-slate-100 flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-emerald-500 dark:text-emerald-400" />
          <span>Audit Trail & Compliance Log</span>
        </h3>
        <button className="flex items-center space-x-2 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 border border-slate-200 dark:border-slate-800 px-3 py-1.5 rounded-lg bg-white dark:bg-slate-900/60">
          <FileSpreadsheet className="w-4 h-4" />
          <span>Export CSV</span>
        </button>
      </div>

      <div className="space-y-2">
        {logs.map((log, idx) => (
          <div key={idx} className="p-3 rounded-xl bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 text-xs flex items-center justify-between">
            <div>
              <span className="font-mono text-indigo-500 dark:text-indigo-400 font-medium">[{log.agent}]</span>{' '}
              <span className="text-slate-600 dark:text-slate-300">{log.details}</span>
            </div>
            <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500">{log.timestamp}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
