import React, { useState } from 'react';
import { UploadDropzone } from '../components/UploadDropzone';
import { api } from '../services/api';

interface NewMigrationProps {
  onNavigate: (page: string, jobId?: string) => void;
}

export const NewMigration: React.FC<NewMigrationProps> = ({ onNavigate }) => {
  const [clientName, setClientName] = useState('ABC Retail Store');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const clientId = `client_${clientName.toLowerCase().replace(/\s+/g, '_')}`;
      const newJob = await api.createJob(clientId, clientName);
      onNavigate('detail', newJob.job_id);
    } catch {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold gradient-text">Start New Data Migration</h1>
        <p className="text-xs text-slate-400 mt-1">
          Upload legacy records to initialize the Google ADK Agent Swarm pipeline.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="glass-card p-6 space-y-6">
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Target Client / Organization Name
          </label>
          <input
            type="text"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            required
            className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 transition-colors"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Upload Legacy Files (Scans, PDFs, Excel)
          </label>
          <UploadDropzone />
        </div>

        <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
          <button
            type="button"
            onClick={() => onNavigate('dashboard')}
            className="py-2.5 px-4 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="py-2.5 px-6 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/20 disabled:opacity-50 transition-all duration-200"
          >
            {isSubmitting ? 'Initializing Agent Swarm...' : 'Launch Agent Pipeline'}
          </button>
        </div>
      </form>
    </div>
  );
};
