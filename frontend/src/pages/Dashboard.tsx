import React, { useEffect, useState } from 'react';
import { MigrationJob } from '../types';
import { api } from '../services/api';
import { PlusCircle, Layers, CheckCircle2, Clock, Download } from 'lucide-react';
import { exportToExcel } from '../utils/excelExport';

interface DashboardProps {
  onNavigate: (page: string, jobId?: string) => void;
}

const CATEGORY_LABELS: Record<string, string> = {
  sales: 'Sales',
  expenses: 'Expenses',
  payroll: 'Payroll',
  invoices: 'Invoices',
  purchases: 'Purchases',
  other: 'Other',
};

export const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [jobs, setJobs] = useState<MigrationJob[]>([]);

  useEffect(() => {
    api.getJobs().then(setJobs).catch(() => setJobs([]));
  }, []);

  const handleExport = () => {
    exportToExcel(
      jobs.map((j) => ({
        client_name: j.client_name,
        job_id: j.job_id,
        data_category: CATEGORY_LABELS[j.data_category] || j.data_category,
        status: j.status,
        total_documents: j.total_documents,
        processed_documents: j.processed_documents,
        total_records_detected: j.total_records_detected,
        records_imported: j.records_imported,
        anomalies_found: j.anomalies_found,
        clarifications_pending: j.clarifications_pending,
        created_at: j.created_at,
        updated_at: j.updated_at,
      })),
      {
        fileName: 'migration-jobs',
        sheetName: 'Migration Jobs',
        columns: [
          { key: 'client_name', label: 'Client Name' },
          { key: 'job_id', label: 'Job ID' },
          { key: 'data_category', label: 'Data Category' },
          { key: 'status', label: 'Status' },
          { key: 'total_documents', label: 'Total Documents' },
          { key: 'processed_documents', label: 'Processed Documents' },
          { key: 'total_records_detected', label: 'Total Records Detected' },
          { key: 'records_imported', label: 'Records Imported' },
          { key: 'anomalies_found', label: 'Anomalies Found' },
          { key: 'clarifications_pending', label: 'Clarifications Pending' },
          { key: 'created_at', label: 'Created At' },
          { key: 'updated_at', label: 'Updated At' },
        ],
      },
    );
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold gradient-text">Migration Dashboard</h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Autonomous data ingestion & ERP schema migration status overview
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleExport}
            disabled={jobs.length === 0}
            className="flex items-center justify-center space-x-2 py-2.5 px-5 rounded-xl text-xs font-semibold text-indigo-600 dark:text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 hover:bg-indigo-500/20 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200"
          >
            <Download className="w-4 h-4" />
            <span>Export Excel</span>
          </button>
          <button
            onClick={() => onNavigate('new')}
            className="flex items-center justify-center space-x-2 py-2.5 px-5 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/25 transition-all duration-200"
          >
            <PlusCircle className="w-4 h-4" />
            <span>New Migration Job</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="glass-card p-5 flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400">Total Jobs</p>
            <p className="text-xl font-bold text-slate-900 dark:text-slate-100">{jobs.length}</p>
          </div>
        </div>

        <div className="glass-card p-5 flex items-center space-x-4">
          <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400">Records Imported</p>
            <p className="text-xl font-bold text-slate-900 dark:text-slate-100">
              {jobs.reduce((acc, j) => acc + j.records_imported, 0)}
            </p>
          </div>
        </div>
      </div>

      <div className="glass-card p-6 space-y-4">
        <h3 className="text-base font-semibold text-slate-800 dark:text-slate-200">Recent Migration Jobs</h3>
        {jobs.length === 0 ? (
          <div className="py-12 text-center text-slate-400 dark:text-slate-500 text-xs">
            No active migration jobs found. Click "New Migration Job" to start.
          </div>
        ) : (
          <div className="space-y-3">
            {jobs.map((job) => (
              <div
                key={job.job_id}
                onClick={() => onNavigate('detail', job.job_id)}
                className="flex items-center justify-between p-4 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/50 cursor-pointer transition-all duration-200"
              >
                <div>
                  <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200">{job.client_name}</h4>
                  <p className="text-xs text-slate-500 dark:text-slate-400 font-mono mt-0.5">{job.job_id}</p>
                </div>
                <div className="flex items-center space-x-4">
                  <span className="text-xs px-3 py-1 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                    {CATEGORY_LABELS[job.data_category] || job.data_category}
                  </span>
                  <span className="text-xs px-3 py-1 rounded-full font-mono bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
                    {job.status}
                  </span>
                  <Clock className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
