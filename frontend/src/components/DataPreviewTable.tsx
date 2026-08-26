import React, { useEffect, useMemo, useState } from 'react';
import { DataPreview, MappingEntry } from '../types';
import { CheckCircle2, AlertTriangle, Database, Plus, Trash2, Save, Code2, Download } from 'lucide-react';
import { api } from '../services/api';
import { exportToExcel } from '../utils/excelExport';

interface DataPreviewTableProps {
  preview: DataPreview;
  onApprove?: () => void;
  onUpdated?: (preview: DataPreview) => void;
}

const COLUMN_LABELS: Record<string, string> = {
  sale_date: 'Sale Date',
  customer_name: 'Customer Name',
  product_name: 'Product Name',
  quantity: 'Quantity',
  unit_price: 'Unit Price',
  total_amount: 'Total Amount',
  expense_date: 'Expense Date',
  vendor_name: 'Vendor Name',
  category: 'Category',
  description: 'Description',
  amount: 'Amount',
  pay_date: 'Pay Date',
  employee_name: 'Employee Name',
  role: 'Role',
  hours_worked: 'Hours Worked',
  hourly_rate: 'Hourly Rate',
  gross_pay: 'Gross Pay',
  deductions: 'Deductions',
  net_pay: 'Net Pay',
  invoice_date: 'Invoice Date',
  invoice_number: 'Invoice #',
  due_date: 'Due Date',
  subtotal: 'Subtotal',
  tax: 'Tax',
  total_due: 'Total Due',
  purchase_date: 'Purchase Date',
  supplier_name: 'Supplier Name',
  item_name: 'Item Name',
  unit_cost: 'Unit Cost',
  total_cost: 'Total Cost',
};

const CURRENCY_FIELDS = new Set([
  'unit_price', 'total_amount', 'amount', 'hourly_rate', 'gross_pay', 'deductions',
  'net_pay', 'subtotal', 'tax', 'total_due', 'unit_cost', 'total_cost',
]);

const MappingPanel: React.FC<{ mappings: MappingEntry[] }> = ({ mappings }) => {
  if (!mappings || mappings.length === 0) return null;

  return (
    <div className="rounded-xl border border-indigo-500/20 bg-indigo-500/5 p-4">
      <h4 className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider flex items-center space-x-2 mb-3">
        <Code2 className="w-4 h-4" />
        <span>Agent Column Mapping (JSON)</span>
      </h4>

      <div className="space-y-2">
        {mappings.map((m) => (
          <div key={m.document_id} className="rounded-lg bg-white dark:bg-slate-950/50 border border-slate-200 dark:border-slate-800">
            <div className="px-3 py-2 text-xs font-medium text-slate-700 dark:text-slate-200 font-mono border-b border-slate-100 dark:border-slate-800/60">
              {m.file_name}
            </div>
            <pre className="text-[11px] font-mono text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-900/60 p-3 rounded-b-lg overflow-x-auto">
              {JSON.stringify(m.mappings, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
};

export const DataPreviewTable: React.FC<DataPreviewTableProps> = ({ preview, onApprove, onUpdated }) => {
  const [records, setRecords] = useState<Record<string, unknown>[]>([]);
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);

  // Sync editable state when the preview changes
  useEffect(() => {
    const source = preview.records && preview.records.length > 0 ? preview.records : preview.sample_records;
    setRecords(source.map((r) => ({ ...r })));
  }, [preview]);

  const columns = useMemo(() => {
    const schemaCols = preview.target_schema?.columns?.filter(Boolean) ?? [];
    const extra = new Set<string>();
    records.forEach((r) => Object.keys(r).forEach((k) => extra.add(k)));
    const seen = new Set<string>();
    const ordered: string[] = [];
    [...schemaCols, ...Array.from(extra)].forEach((c) => {
      if (!seen.has(c)) {
        seen.add(c);
        ordered.push(c);
      }
    });
    return ordered;
  }, [records, preview.target_schema]);

  const handleCellChange = (rowIdx: number, col: string, value: string) => {
    setRecords((prev) => {
      const next = prev.map((r, i) => (i === rowIdx ? { ...r, [col]: value } : r));
      return next;
    });
    setSaveStatus(null);
  };

  const addRow = () => {
    const blank: Record<string, unknown> = {};
    columns.forEach((c) => { blank[c] = ''; });
    setRecords((prev) => [...prev, blank]);
    setSaveStatus(null);
  };

  const deleteRow = (rowIdx: number) => {
    setRecords((prev) => prev.filter((_, i) => i !== rowIdx));
    setSaveStatus(null);
  };

  const handleSave = async () => {
    setSaving(true);
    setSaveStatus(null);
    try {
      const updated = await api.savePreviewRecords(preview.job_id, records);
      setSaveStatus(`Saved ${records.length} records`);
      onUpdated?.(updated);
    } catch (err) {
      setSaveStatus('Failed to save edits');
    } finally {
      setSaving(false);
    }
  };

  const handleExport = () => {
    const exportColumns = columns.map((key) => ({
      key,
      label: COLUMN_LABELS[key] || key,
    }));
    exportToExcel(records, {
      fileName: `migration-${preview.job_id}-data`,
      sheetName: preview.target_schema?.label || 'Data',
      columns: exportColumns,
    });
  };

  const formatCell = (col: string, value: unknown): string => {
    if (value === null || value === undefined) return '';
    if (CURRENCY_FIELDS.has(col) && typeof value === 'number') {
      return String(value);
    }
    return String(value);
  };

  return (
    <div className="glass-card p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100 flex items-center space-x-2">
            <Database className="w-5 h-5 text-indigo-500 dark:text-indigo-400" />
            <span>{preview.target_schema?.label || 'Data'} Preview — Editable</span>
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Edit cells like a spreadsheet, then save and import to Uniplexity ERP.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-xs text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20">
            <CheckCircle2 className="w-4 h-4" />
            <span>{records.length} Records</span>
          </div>
          <div className="flex items-center space-x-2 text-xs text-amber-600 dark:text-amber-400 bg-amber-500/10 px-3 py-1.5 rounded-lg border border-amber-500/20">
            <AlertTriangle className="w-4 h-4" />
            <span>{preview.anomalies.length} Anomalies</span>
          </div>
          <button
            type="button"
            onClick={handleExport}
            disabled={records.length === 0}
            title="Download extracted data as Excel"
            className="flex items-center space-x-1.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 px-3 py-1.5 rounded-lg shadow-lg shadow-indigo-600/20 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200"
          >
            <Download className="w-4 h-4" />
            <span>Export Excel</span>
          </button>
        </div>
      </div>

      <MappingPanel mappings={preview.mappings || []} />

      <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-xl">
        <table className="w-full text-left text-xs text-slate-600 dark:text-slate-300">
          <thead className="bg-slate-100 dark:bg-slate-900/80 text-slate-500 dark:text-slate-400 uppercase font-semibold border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th className="px-2 py-3 w-8"></th>
              {columns.map((col) => (
                <th key={col} className="px-2 py-3 whitespace-nowrap min-w-[110px]">{COLUMN_LABELS[col] || col}</th>
              ))}
              <th className="px-2 py-3 w-10"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800/60 bg-white dark:bg-slate-950/40">
            {records.map((row, rowIdx) => (
              <tr key={rowIdx} className="hover:bg-slate-50 dark:hover:bg-slate-900/60 transition-colors">
                <td className="px-2 py-1 text-slate-400 dark:text-slate-600 font-mono text-[10px]">{rowIdx + 1}</td>
                {columns.map((col) => (
                  <td key={col} className="px-2 py-1">
                    <input
                      value={formatCell(col, row[col])}
                      onChange={(e) => handleCellChange(rowIdx, col, e.target.value)}
                      className={`w-full px-2 py-1.5 rounded-lg bg-transparent border border-transparent focus:border-indigo-500/60 focus:bg-white dark:focus:bg-slate-900 focus:outline-none text-xs transition-colors ${
                        CURRENCY_FIELDS.has(col) ? 'font-semibold text-indigo-500 dark:text-indigo-400' : 'text-slate-700 dark:text-slate-200'
                      }`}
                    />
                  </td>
                ))}
                <td className="px-2 py-1">
                  <button
                    type="button"
                    onClick={() => deleteRow(rowIdx)}
                    title="Delete row"
                    className="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-500/10 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
            {records.length === 0 && (
              <tr>
                <td colSpan={columns.length + 2} className="px-4 py-8 text-center text-slate-400 dark:text-slate-500">
                  No records to display. Click "Add Row" to create one.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center space-x-2">
          <button
            type="button"
            onClick={addRow}
            className="py-2 px-4 rounded-xl text-xs font-semibold text-indigo-600 dark:text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 hover:bg-indigo-500/20 transition-all duration-200 flex items-center space-x-1.5"
          >
            <Plus className="w-4 h-4" />
            <span>Add Row</span>
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={saving}
            className="py-2 px-4 rounded-xl text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 transition-all duration-200 flex items-center space-x-1.5"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Saving...' : 'Save Edits'}</span>
          </button>
          {saveStatus && (
            <span className="text-xs text-slate-500 dark:text-slate-400">{saveStatus}</span>
          )}
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
  );
};
