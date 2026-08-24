import { useState } from 'react';
import { ThemeToggle } from './components/ThemeToggle';
import { Dashboard } from './pages/Dashboard';
import { NewMigration } from './pages/NewMigration';
import { MigrationDetail } from './pages/MigrationDetail';
import { ClarificationCenter } from './pages/ClarificationCenter';
import { Database, LayoutDashboard, PlusCircle, HelpCircle } from 'lucide-react';

export function App() {
  const [currentPage, setCurrentPage] = useState<string>('dashboard');
  const [selectedJobId, setSelectedJobId] = useState<string>('');

  const navigate = (page: string, jobId?: string) => {
    setCurrentPage(page);
    if (jobId) {
      setSelectedJobId(jobId);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col font-sans">
      {/* Top Navbar */}
      <header className="border-b border-slate-200 dark:border-slate-800/80 bg-white/80 dark:bg-slate-900/60 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('dashboard')}>
            <div className="p-2 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-500 text-white shadow-lg shadow-indigo-500/25">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-base text-slate-900 dark:text-slate-100 tracking-tight">Uniplexity</span>
              <span className="text-xs text-indigo-500 dark:text-indigo-400 font-semibold ml-1.5 px-2 py-0.5 rounded-full bg-indigo-500/10 border border-indigo-500/20">
                Migration Agent
              </span>
            </div>
          </div>

          <nav className="flex items-center space-x-1 sm:space-x-2">
            <ThemeToggle />
            <button
              onClick={() => navigate('dashboard')}
              className={`flex items-center space-x-2 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                currentPage === 'dashboard'
                  ? 'bg-indigo-600/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-900/40'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span className="hidden sm:inline">Dashboard</span>
            </button>

            <button
              onClick={() => navigate('new')}
              className={`flex items-center space-x-2 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                currentPage === 'new'
                  ? 'bg-indigo-600/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-900/40'
              }`}
            >
              <PlusCircle className="w-4 h-4" />
              <span className="hidden sm:inline">New Job</span>
            </button>

            <button
              onClick={() => navigate('clarification')}
              className={`flex items-center space-x-2 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                currentPage === 'clarification'
                  ? 'bg-indigo-600/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-900/40'
              }`}
            >
              <HelpCircle className="w-4 h-4" />
              <span className="hidden sm:inline">Clarification Center</span>
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentPage === 'dashboard' && <Dashboard onNavigate={navigate} />}
        {currentPage === 'new' && <NewMigration onNavigate={navigate} />}
        {currentPage === 'detail' && <MigrationDetail jobId={selectedJobId} onNavigate={navigate} />}
        {currentPage === 'clarification' && <ClarificationCenter />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-900 py-6 text-center text-xs text-slate-400 dark:text-slate-500">
        Google Cloud — All Things Agentic Hackathon Submission &bull; Powered by Google ADK & Vertex AI Gemini
      </footer>
    </div>
  );
}

export default App;
