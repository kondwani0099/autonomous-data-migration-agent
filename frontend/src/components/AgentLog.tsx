import React from 'react';
import { AuditLogEntry } from '../types';
import { Bot, ChevronRight } from 'lucide-react';

interface AgentLogProps {
  entries: AuditLogEntry[];
}

export const AgentLog: React.FC<AgentLogProps> = ({ entries }) => {
  return (
    <div className="glass-card p-6 space-y-4">
      <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-200 flex items-center space-x-2">
        <Bot className="w-4 h-4 text-indigo-500 dark:text-indigo-400" />
        <span>Agent Action Log</span>
      </h4>

      <div className="space-y-3">
        {entries.length === 0 ? (
          <p className="text-xs text-slate-400 dark:text-slate-500 italic">No agent actions recorded yet.</p>
        ) : (
          entries.map((entry, idx) => (
            <div key={idx} className="flex items-start space-x-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800 text-xs">
              <ChevronRight className="w-4 h-4 text-indigo-500 dark:text-indigo-400 mt-0.5 flex-shrink-0" />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-indigo-500 dark:text-indigo-300">{entry.agent}</span>
                  <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500">{entry.timestamp}</span>
                </div>
                <p className="text-slate-600 dark:text-slate-300 mt-1">{entry.details}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
