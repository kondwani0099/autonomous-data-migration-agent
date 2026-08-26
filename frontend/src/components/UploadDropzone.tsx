import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, FolderOpen } from 'lucide-react';

interface UploadDropzoneProps {
  onFilesSelected?: (files: File[]) => void;
}

const SUPPORTED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'xlsx', 'xls', 'csv'];

const isSupportedFile = (file: File): boolean => {
  const ext = file.name.split('.').pop()?.toLowerCase() || '';
  return SUPPORTED_EXTENSIONS.includes(ext);
};

// Recursively traverse a dropped FileSystemEntry (file or directory) and
// collect all files with their relative paths.
const traverseFileTree = async (
  entry: any,
  path = '',
): Promise<{ file: File; path: string }[]> => {
  const results: { file: File; path: string }[] = [];

  if (entry.isFile) {
    const file = await new Promise<File>((resolve, reject) => entry.file(resolve, reject));
    results.push({ file, path: path || file.name });
  } else if (entry.isDirectory) {
    const reader = entry.createReader();
    // readEntries must be called repeatedly until it returns an empty array.
    let batch: any[] = [];
    do {
      batch = await new Promise<any[]>((resolve, reject) => reader.readEntries(resolve, reject));
      for (const child of batch) {
        results.push(...(await traverseFileTree(child, path ? `${path}/${child.name}` : child.name)));
      }
    } while (batch.length > 0);
  }

  return results;
};

export const UploadDropzone: React.FC<UploadDropzoneProps> = ({ onFilesSelected }) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  const commitFiles = (files: File[]) => {
    const supported = files.filter(isSupportedFile);
    setSelectedFiles(supported);
    if (onFilesSelected) {
      onFilesSelected(supported);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      commitFiles(Array.from(e.target.files));
    }
    // Reset so selecting the same file/folder again re-fires onChange
    e.target.value = '';
  };

  // Folder selection via <input webkitdirectory>
  const handleFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      commitFiles(Array.from(e.target.files));
    }
    e.target.value = '';
  };

  // Drag & drop (files AND folders)
  const handleDrop = async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const items = e.dataTransfer?.items;
    if (items && items.length > 0 && typeof items[0].webkitGetAsEntry === 'function') {
      // Traverse directories for folder drops
      const collected: { file: File; path: string }[] = [];
      for (const item of Array.from(items)) {
        const entry = item.webkitGetAsEntry();
        if (entry) {
          collected.push(...(await traverseFileTree(entry)));
        }
      }
      commitFiles(collected.map((f) => f.file));
      return;
    }

    // Fallback: plain file drop
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      commitFiles(Array.from(files));
    }
  };

  return (
    <div className="w-full space-y-3">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-2xl cursor-pointer bg-slate-50 dark:bg-slate-900/40 transition-all duration-300 group ${
          isDragging
            ? 'border-indigo-500 bg-indigo-500/10 dark:bg-indigo-500/10 scale-[1.01]'
            : 'border-slate-300 dark:border-slate-700/80 hover:bg-slate-100 dark:hover:bg-slate-900/80 hover:border-indigo-500/50'
        }`}
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6 pointer-events-none">
          <div className="p-4 rounded-full bg-indigo-500/10 text-indigo-500 dark:text-indigo-400 group-hover:scale-110 group-hover:bg-indigo-500/20 transition-all duration-300 mb-3">
            <UploadCloud className="w-10 h-10" />
          </div>
          <p className="mb-2 text-sm text-slate-700 dark:text-slate-200 font-medium">
            <span className="font-semibold text-indigo-500 dark:text-indigo-400">Click to upload</span> or drag &amp; drop
          </p>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Scanned ledgers (PNG, JPG), Excel files (.xlsx, .csv), PDFs — or a whole folder
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <label
          htmlFor="file-upload"
          className="flex-1 py-2.5 rounded-xl text-xs font-semibold text-center text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/20 cursor-pointer transition-all duration-200"
        >
          Select Files
        </label>
        <label
          htmlFor="folder-upload"
          className="flex-1 py-2.5 rounded-xl text-xs font-semibold text-center text-indigo-600 dark:text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 hover:bg-indigo-500/20 cursor-pointer transition-all duration-200 flex items-center justify-center space-x-1.5"
        >
          <FolderOpen className="w-4 h-4" />
          <span>Upload Folder</span>
        </label>
      </div>

      <input
        id="file-upload"
        type="file"
        multiple
        accept=".pdf,.png,.jpg,.jpeg,.xlsx,.xls,.csv"
        className="hidden"
        onChange={handleFileChange}
      />
      <input
        id="folder-upload"
        type="file"
        multiple
        {...({ webkitdirectory: '', directory: '' } as React.InputHTMLAttributes<HTMLInputElement>)}
        className="hidden"
        onChange={handleFolderChange}
      />

      {selectedFiles.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
            Selected Files ({selectedFiles.length})
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-52 overflow-y-auto pr-1">
            {selectedFiles.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center space-x-3 p-3 glass-card bg-white dark:bg-slate-900/80 text-xs text-slate-700 dark:text-slate-200"
              >
                <FileText className="w-4 h-4 text-indigo-500 dark:text-indigo-400 flex-shrink-0" />
                <span className="truncate flex-1 font-medium">{file.name}</span>
                <CheckCircle2 className="w-4 h-4 text-emerald-500 dark:text-emerald-400 flex-shrink-0" />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
