import React, { useState } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function ProjectSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResults(null);
    try {
      const res = await axios.post(`${API}/similar-projects`, {
        query: query.trim(),
        top_k: 5,
      });
      setResults(res.data);
    } catch (err) {
      setError('Failed to search projects. Make sure the backend is running.');
    }
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSearch();
  };

  return (
    <div className="card">
      <h2 className="card-title">🔍 AI Project Similarity Search</h2>
      <p className="card-subtitle">
        Enter a project idea to find similar existing projects using AI embeddings
      </p>

      <div className="search-container">
        <span className="search-icon">🔎</span>
        <input
          id="search-input"
          type="text"
          className="search-input"
          placeholder="e.g. Solar panel fault detection using deep learning"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>

      <button
        id="search-btn"
        className="search-btn"
        onClick={handleSearch}
        disabled={loading || !query.trim()}
      >
        {loading ? '⏳ Searching...' : '🚀 Find Similar Projects'}
      </button>

      {error && <div className="error-msg" style={{ marginTop: 16 }}>{error}</div>}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <span>Computing embeddings and finding similar projects...</span>
        </div>
      )}

      {results && !loading && (
        <div style={{ marginTop: 24 }}>
          <div className="section-header">
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Similar Projects</h3>
            <span className="section-count">
              {results.results.length} result{results.results.length !== 1 ? 's' : ''} found
            </span>
          </div>

          {results.results.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📭</div>
              <p>No similar projects found. Try a different query.</p>
            </div>
          ) : (
            <div className="results-grid">
              {results.results.map((project, i) => (
                <div key={project.id} className="result-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12 }}>
                    <div className="result-title">{project.title}</div>
                    <span className="similarity-badge">
                      ✨ {(project.similarity_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="result-meta">
                    <span>👤 {project.authors.join(', ')}</span>
                    <span>📅 {project.year}</span>
                    <span className="tag domain">{project.domain}</span>
                  </div>
                  <p className="result-abstract">{project.abstract}</p>
                  <div className="tags">
                    {project.technologies.map(tech => (
                      <span key={tech} className="tag">{tech}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!results && !loading && !error && (
        <div className="empty-state" style={{ marginTop: 40 }}>
          <div className="empty-icon">🔬</div>
          <p>Enter a project idea above to discover similar projects</p>
        </div>
      )}
    </div>
  );
}

export default ProjectSearch;
