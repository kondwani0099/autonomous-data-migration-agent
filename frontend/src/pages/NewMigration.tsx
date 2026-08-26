import React, { useEffect, useState } from 'react';
import { UploadDropzone } from '../components/UploadDropzone';
import { api } from '../services/api';
import { DataCategory, DataCategoryOption } from '../types';
import { TrendingUp, Wallet, Users, FileText, ShoppingCart, Check } from 'lucide-react';

interface NewMigrationProps {
  onNavigate: (page: string, jobId?: string) => void;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  sales: <TrendingUp className="w-5 h-5" />,
  expenses: <Wallet className="w-5 h-5" />,
  payroll: <Users className="w-5 h-5" />,
  invoices: <FileText className="w-5 h-5" />,
  purchases: <ShoppingCart className="w-5 h-5" />,
};

export const NewMigration: React.FC<NewMigrationProps> = ({ onNavigate }) => {
  const [clientName, setClientName] = useState('ABC Retail Store');
  const [categories, setCategories] = useState<DataCategoryOption[]>([]);
  const [dataCategory, setDataCategory] = useState<DataCategory>('sales');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  useEffect(() => {
    api.getDataCategories().then(setCategories).catch(() => {});
  }, []);

  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles(files);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setUploadError(null);
    try {
      const clientId = `client_${clientName.toLowerCase().replace(/\s+/g, '_')}`;
      const newJob = await api.createJob(clientId, clientName, dataCategory);

      // Upload files if any were selected
      if (selectedFiles.length > 0) {
        try {
          await api.uploadFiles(newJob.job_id, selectedFiles);
        } catch (err: any) {
          console.error('Upload failed:', err);
          setUploadError(err?.response?.data?.detail || 'File upload failed. Please try again.');
          setIsSubmitting(false);
          return;
        }
      }

      onNavigate('detail', newJob.job_id);
    } catch {
      setIsSubmitting(false);
    }
  };

  const selectedCategory = categories.find((c) => c.value === dataCategory);

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold gradient-text">Start New Data Migration</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Upload legacy records to initialize the Google ADK Agent Swarm pipeline.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="glass-card p-6 space-y-6">
        <div>
          <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-2">
            Target Client / Organization Name
          </label>
          <input
            type="text"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            required
            className="w-full px-4 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:border-indigo-500 transition-colors"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-2">
            Data Format (Agents will normalize into this structure)
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {categories.map((cat) => {
              const isActive = cat.value === dataCategory;
              return (
                <button
                  key={cat.value}
                  type="button"
                  onClick={() => setDataCategory(cat.value as DataCategory)}
                  className={`flex items-start space-x-3 p-3 rounded-xl border text-left transition-all duration-200 ${
                    isActive
                      ? 'bg-indigo-600/10 border-indigo-500/40 dark:border-indigo-500/50 ring-1 ring-indigo-500/30'
                      : 'bg-slate-50 dark:bg-slate-950/40 border-slate-200 dark:border-slate-800 hover:border-indigo-400/40'
                  }`}
                >
                  <div className={`p-2 rounded-lg flex-shrink-0 ${isActive ? 'bg-indigo-500 text-white' : 'bg-slate-200 dark:bg-slate-800 text-slate-500 dark:text-slate-400'}`}>
                    {CATEGORY_ICONS[cat.value]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-slate-800 dark:text-slate-100">{cat.label}</span>
                      {isActive && <Check className="w-4 h-4 text-indigo-500" />}
                    </div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">{cat.description}</p>
                  </div>
                </button>
              );
            })}
          </div>
          {selectedCategory && selectedCategory.columns.length > 0 && (
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-2">
              Target fields: <span className="font-mono text-indigo-500 dark:text-indigo-400">{selectedCategory.columns.join(', ')}</span>
            </p>
          )}
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider mb-2">
            Upload Legacy Files (Scans, PDFs, Excel)
          </label>
          <UploadDropzone onFilesSelected={handleFilesSelected} />
        </div>

        {uploadError && (
          <div className="p-3 rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900 text-xs text-red-600 dark:text-red-400">
            {uploadError}
          </div>
        )}

        <div className="flex justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
          <button
            type="button"
            onClick={() => onNavigate('dashboard')}
            className="py-2.5 px-4 rounded-xl text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="py-2.5 px-6 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/20 disabled:opacity-50 transition-all duration-200"
          >
            {isSubmitting ? 'Uploading & Processing...' : 'Launch Agent Pipeline'}
          </button>
        </div>
      </form>
    </div>
  );
};
