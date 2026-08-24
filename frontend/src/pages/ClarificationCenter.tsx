import React from 'react';
import { HelpCircle } from 'lucide-react';

export const ClarificationCenter: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold gradient-text">Clarification Center</h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Review and answer agent questions across all active migration jobs.
        </p>
      </div>

      <div className="glass-card p-12 text-center space-y-3">
        <div className="p-4 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 w-fit mx-auto">
          <HelpCircle className="w-8 h-8" />
        </div>
        <h3 className="text-base font-semibold text-slate-700 dark:text-slate-200">No Pending Clarifications</h3>
        <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
          All agent schema mappings are operating at high confidence (&gt;70%). New questions will appear here automatically.
        </p>
      </div>
    </div>
  );
};
