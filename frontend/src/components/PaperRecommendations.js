import React, { useState } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function PaperRecommendations() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await axios.post(`${API}/research-papers`, {
        query: query.trim(),
      });
      setResult(res.data);
    } catch (err) {
      setError('Failed to fetch papers. Make sure the backend is running.');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2 className="card-title">📄 Research Paper Recommendations</h2>
      <p className="card-subtitle">
        Discover relevant research papers from Semantic Scholar and arXiv
      </p>

      <div className="search-container">
        <span className="search-icon">📖</span>
        <input
          id="paper-input"
          type="text"
          className="search-input"
          placeholder="e.g. AI agriculture crop disease detection"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
      </div>

      <button
        id="paper-btn"
        className="search-btn"
        onClick={handleSearch}
        disabled={loading || !query.trim()}
      >
        {loading ? '⏳ Searching...' : '📚 Find Papers'}
      </button>

      {error && <div className="error-msg" style={{ marginTop: 16 }}>{error}</div>}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <span>Querying research paper databases...</span>
        </div>
      )}

      {result && !loading && (
        <div style={{ marginTop: 24 }}>
          <div className="section-header">
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>
              Papers related to "{result.query}"
            </h3>
            <span className="section-count">
              Source: {result.source} • {result.papers.length} paper{result.papers.length !== 1 ? 's' : ''}
            </span>
          </div>

          {result.error && (
            <div className="error-msg" style={{ marginBottom: 16 }}>{result.error}</div>
          )}

          {result.papers.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📭</div>
              <p>No papers found. Try a different query.</p>
            </div>
          ) : (
            <div>
              {result.papers.map((paper, i) => (
                <div key={i} className="paper-item">
                  <div className="paper-title">
                    {paper.url ? (
                      <a href={paper.url} target="_blank" rel="noopener noreferrer">
                        {paper.title}
                      </a>
                    ) : (
                      paper.title
                    )}
                  </div>
                  <div className="paper-authors">
                    {paper.authors.join(', ')}
                    {paper.authors.length === 3 && ' et al.'}
                  </div>
                  {paper.abstract && (
                    <p className="paper-abstract">{paper.abstract}</p>
                  )}
                  <div className="paper-meta">
                    {paper.year && <span>📅 {paper.year}</span>}
                    {paper.citations != null && <span>📊 {paper.citations} citations</span>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!result && !loading && !error && (
        <div className="empty-state" style={{ marginTop: 40 }}>
          <div className="empty-icon">📚</div>
          <p>Enter a research topic to discover relevant papers</p>
        </div>
      )}
    </div>
  );
}

export default PaperRecommendations;
