import React, { useState } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function IdeaImprover() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleImprove = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await axios.post(`${API}/idea-improvement`, {
        query: query.trim(),
      });
      setResult(res.data);
    } catch (err) {
      setError('Failed to generate improvements. Make sure the backend is running.');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2 className="card-title">💡 AI Idea Improvement Generator</h2>
      <p className="card-subtitle">
        Enter a project idea and get AI-powered improvement suggestions
      </p>

      <div className="search-container">
        <span className="search-icon">💭</span>
        <input
          id="idea-input"
          type="text"
          className="search-input"
          placeholder="e.g. Smart irrigation system"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleImprove()}
        />
      </div>

      <button
        id="improve-btn"
        className="search-btn"
        onClick={handleImprove}
        disabled={loading || !query.trim()}
      >
        {loading ? '⏳ Generating...' : '✨ Generate Improvements'}
      </button>

      {error && <div className="error-msg" style={{ marginTop: 16 }}>{error}</div>}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <span>AI is analyzing your idea and generating improvements...</span>
        </div>
      )}

      {result && !loading && (
        <div style={{ marginTop: 24 }}>
          <div className="section-header">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>
              Suggested Improvements for "{result.idea}"
            </h3>
            <span className={`method-badge ${result.method}`}>
              {result.method === 'llm' ? '🤖 LLM' : '📋 Rule-based'}
            </span>
          </div>

          <ul className="improvement-list">
            {result.improvements.map((imp, i) => (
              <li key={i} className="improvement-item">
                <span className="improvement-icon">💎</span>
                <span className="improvement-text">{imp}</span>
              </li>
            ))}
          </ul>

          {result.categories_detected && (
            <div style={{ marginTop: 16 }}>
              <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginRight: 8 }}>
                Categories detected:
              </span>
              <div className="tags" style={{ display: 'inline-flex' }}>
                {result.categories_detected.map(cat => (
                  <span key={cat} className="tag">{cat}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {!result && !loading && !error && (
        <div className="empty-state" style={{ marginTop: 40 }}>
          <div className="empty-icon">🧠</div>
          <p>Enter your project idea above to get AI-powered suggestions</p>
        </div>
      )}
    </div>
  );
}

export default IdeaImprover;
