import React from 'react';
import { DataPreview } from '../types';
import { CheckCircle2, AlertTriangle, Database } from 'lucide-react';

interface DataPreviewTableProps {
  preview: DataPreview;
  onApprove?: () => void;
}

export const DataPreviewTable: React.FC<DataPreviewTableProps> = ({ preview, onApprove }) => {
  return (
    <div className="glass-card p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100 flex items-center space-x-2">
            <Database className="w-5 h-5 text-indigo-500 dark:text-indigo-400" />
            <span>Dry-Run Data Migration Preview</span>
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Review normalized records and anomalies prior to committing to Uniplexity ERP.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-xs text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20">
            <CheckCircle2 className="w-4 h-4" />
            <span>{preview.clean_count} Clean Records</span>
          </div>

          <div className="flex items-center space-x-2 text-xs text-amber-600 dark:text-amber-400 bg-amber-500/10 px-3 py-1.5 rounded-lg border border-amber-500/20">
            <AlertTriangle className="w-4 h-4" />
            <span>{preview.anomalies.length} Anomalies</span>
          </div>

          {onApprove && (
            <button
              onClick={onApprove}
              className="py-2 px-5 rounded-xl text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/20 transition-all duration-200"
            >
              Approve & Import to ERP
            </button>
          )}
        </div>
      </div>

      <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-xl">
        <table className="w-full text-left text-xs text-slate-600 dark:text-slate-300">
          <thead className="bg-slate-100 dark:bg-slate-900/80 text-slate-500 dark:text-slate-400 uppercase font-semibold border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th className="px-4 py-3">Sale Date</th>
              <th className="px-4 py-3">Customer Name</th>
              <th className="px-4 py-3">Product Name</th>
              <th className="px-4 py-3">Quantity</th>
              <th className="px-4 py-3">Unit Price</th>
              <th className="px-4 py-3">Total Amount</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60 bg-white dark:bg-slate-950/40">
            {preview.sample_records.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-900/60 transition-colors">
                <td className="px-4 py-3 font-mono text-slate-500 dark:text-slate-400">{String(row.sale_date || '')}</td>
                <td className="px-4 py-3 font-medium text-slate-800 dark:text-slate-200">{String(row.customer_name || '')}</td>
                <td className="px-4 py-3">{String(row.product_name || '')}</td>
                <td className="px-4 py-3">{String(row.quantity || 0)}</td>
                <td className="px-4 py-3">${Number(row.unit_price || 0).toFixed(2)}</td>
                <td className="px-4 py-3 font-semibold text-indigo-500 dark:text-indigo-400">${Number(row.total_amount || 0).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
