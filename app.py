
import React, { useState } from 'react';
import { groundSearch } from '../services/geminiService';

const SearchPanel: React.FC = () => {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [result, setResult] = useState<{ text: string, grounding: Array<{title: string, uri: string}> } | null>(null);

  const handleSearch = async () => {
    if (!query.trim() || isSearching) return;

    setIsSearching(true);
    try {
      const data = await groundSearch(query);
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Search failed. Check your API configuration.");
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="flex h-full bg-slate-900/40 overflow-hidden">
      <div className="flex-1 p-8 overflow-y-auto custom-scrollbar">
        <div className="max-w-4xl mx-auto space-y-8">
          <header className="flex flex-col gap-2">
            <h1 className="text-3xl font-bold text-white tracking-tight">Insight Engine</h1>
            <p className="text-slate-400">Deep search research grounded with live Google Search results.</p>
          </header>

          <div className="glass-panel p-4 rounded-3xl border border-slate-700/50 flex gap-4">
            <input 
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="What would you like to research today?"
              className="flex-1 bg-transparent border-none focus:ring-0 text-slate-200 px-4"
            />
            <button 
              onClick={handleSearch}
              disabled={isSearching || !query.trim()}
              className="bg-indigo-600 text-white px-6 py-3 rounded-2xl font-bold hover:bg-indigo-500 disabled:bg-slate-700 transition-all flex items-center gap-2"
            >
              {isSearching ? (
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              )}
              Analyze
            </button>
          </div>

          {result && (
            <div className="space-y-8 animate-fade-in">
              <div className="glass-panel p-8 rounded-3xl border border-slate-700/50 space-y-6">
                <div className="prose prose-invert max-w-none text-slate-200 leading-relaxed whitespace-pre-wrap">
                  {result.text}
                </div>

                {result.grounding.length > 0 && (
                  <div className="border-t border-slate-700/50 pt-6">
                    <h3 className="text-sm font-semibold text-slate-400 mb-4 uppercase tracking-wider">Citations & Sources</h3>
                    <div className="flex flex-wrap gap-3">
                      {result.grounding.map((link, i) => (
                        <a 
                          key={i} 
                          href={link.uri} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 bg-slate-800/50 border border-slate-700/50 px-4 py-2 rounded-xl text-xs text-indigo-400 hover:bg-indigo-500/10 hover:border-indigo-500/30 transition-all"
                        >
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                          </svg>
                          {link.title}
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchPanel;
