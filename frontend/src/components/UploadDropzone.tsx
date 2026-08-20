import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2 } from 'lucide-react';

interface UploadDropzoneProps {
  onFilesSelected?: (files: File[]) => void;
}

export const UploadDropzone: React.FC<UploadDropzoneProps> = ({ onFilesSelected }) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files);
      setSelectedFiles(filesArray);
      if (onFilesSelected) {
        onFilesSelected(filesArray);
      }
    }
  };

  return (
    <div className="w-full">
      <label
        htmlFor="file-upload"
        className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-slate-700/80 rounded-2xl cursor-pointer bg-slate-900/40 hover:bg-slate-900/80 hover:border-indigo-500/50 transition-all duration-300 group"
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          <div className="p-4 rounded-full bg-indigo-500/10 text-indigo-400 group-hover:scale-110 group-hover:bg-indigo-500/20 transition-all duration-300 mb-3">
            <UploadCloud className="w-10 h-10" />
          </div>
          <p className="mb-2 text-sm text-slate-200 font-medium">
            <span className="font-semibold text-indigo-400">Click to upload</span> or drag and drop
          </p>
          <p className="text-xs text-slate-400">
            Scanned ledgers (PNG, JPG), Excel files (.xlsx, .csv), or PDFs
          </p>
        </div>
        <input
          id="file-upload"
          type="file"
          multiple
          accept=".pdf,.png,.jpg,.jpeg,.xlsx,.csv"
          className="hidden"
          onChange={handleFileChange}
        />
      </label>

      {selectedFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Selected Files ({selectedFiles.length})
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {selectedFiles.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center space-x-3 p-3 glass-card bg-slate-900/80 text-xs text-slate-200"
              >
                <FileText className="w-4 h-4 text-indigo-400 flex-shrink-0" />
                <span className="truncate flex-1 font-medium">{file.name}</span>
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
