import React, { useState } from 'react';
import { Clarification } from '../types';
import { HelpCircle, Send } from 'lucide-react';

interface ClarificationCardProps {
  clarification: Clarification;
  onAnswerSubmit: (clarificationId: string, answer: string) => void;
}

export const ClarificationCard: React.FC<ClarificationCardProps> = ({
  clarification,
  onAnswerSubmit,
}) => {
  const [selectedOption, setSelectedOption] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedOption) {
      onAnswerSubmit(clarification.clarification_id, selectedOption);
    }
  };

  return (
    <div className="glass-card p-6 border-amber-500/30 bg-gradient-to-b from-amber-950/20 to-slate-900/60">
      <div className="flex items-start space-x-3 mb-4">
        <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 mt-1">
          <HelpCircle className="w-6 h-6" />
        </div>
        <div>
          <span className="text-xs font-semibold text-amber-400 uppercase tracking-wider">
            Agent Clarification Required ({clarification.agent})
          </span>
          <h4 className="text-base font-medium text-slate-100 mt-1">{clarification.question}</h4>
          <p className="text-xs text-slate-400 mt-1">{clarification.context}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="space-y-2">
          {clarification.options.map((option, idx) => (
            <label
              key={idx}
              className={`flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all duration-200 ${
                selectedOption === option
                  ? 'bg-amber-500/10 border-amber-500/50 text-amber-200'
                  : 'bg-slate-900/40 border-slate-800 text-slate-300 hover:border-slate-700'
              }`}
            >
              <span className="text-xs font-medium">{option}</span>
              <input
                type="radio"
                name={`clarification-${clarification.clarification_id}`}
                value={option}
                checked={selectedOption === option}
                onChange={() => setSelectedOption(option)}
                className="text-amber-500 focus:ring-amber-500 bg-slate-950 border-slate-700"
              />
            </label>
          ))}
        </div>

        <button
          type="submit"
          disabled={!selectedOption}
          className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl font-medium text-xs text-white bg-amber-600 hover:bg-amber-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg shadow-amber-600/20"
        >
          <Send className="w-4 h-4" />
          <span>Submit Answer & Resume Pipeline</span>
        </button>
      </form>
    </div>
  );
};
