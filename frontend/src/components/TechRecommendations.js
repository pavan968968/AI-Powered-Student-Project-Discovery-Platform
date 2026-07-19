import React, { useState } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const TECH_ICONS = {
  'Python': '🐍', 'TensorFlow': '🧠', 'PyTorch': '🔥', 'React': '⚛️',
  'Node.js': '🟢', 'Arduino': '🔌', 'Docker': '🐳', 'AWS': '☁️',
  'Flask': '🌶️', 'FastAPI': '⚡', 'OpenCV': '👁️', 'MQTT': '📡',
  'PostgreSQL': '🐘', 'MongoDB': '🍃', 'Firebase': '🔥', 'Git': '📦',
  'Kubernetes': '☸️', 'Raspberry Pi': '🫐', 'Blockchain': '⛓️',
  'default': '🔧',
};

function TechRecommendations() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRecommend = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await axios.post(`${API}/technology-recommendations`, {
        query: query.trim(),
      });
      setResult(res.data);
    } catch (err) {
      setError('Failed to get recommendations. Make sure the backend is running.');
    }
    setLoading(false);
  };

  const getIcon = (tech) => TECH_ICONS[tech] || TECH_ICONS.default;

  return (
    <div className="card">
      <h2 className="card-title">⚙️ Technology Recommendations</h2>
      <p className="card-subtitle">
        Get AI-powered technology stack suggestions for your project idea
      </p>

      <div className="search-container">
        <span className="search-icon">🛠️</span>
        <input
          id="tech-input"
          type="text"
          className="search-input"
          placeholder="e.g. Food waste detection system"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleRecommend()}
        />
      </div>

      <button
        id="tech-btn"
        className="search-btn"
        onClick={handleRecommend}
        disabled={loading || !query.trim()}
      >
        {loading ? '⏳ Analyzing...' : '🔧 Get Tech Recommendations'}
      </button>

      {error && <div className="error-msg" style={{ marginTop: 16 }}>{error}</div>}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <span>Analyzing your idea and matching technologies...</span>
        </div>
      )}

      {result && !loading && (
        <div style={{ marginTop: 24 }}>
          <div className="section-header">
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>
              Suggested Technologies for "{result.idea}"
            </h3>
            <span className={`method-badge ${result.method}`}>
              {result.method === 'llm' ? '🤖 LLM' : '🔑 Keyword-based'}
            </span>
          </div>

          <div className="tech-grid">
            {result.technologies.map((tech, i) => (
              <div
                key={tech}
                className="tech-item"
                style={{ animationDelay: `${i * 0.05}s` }}
              >
                <span className="tech-icon">{getIcon(tech)}</span>
                <span className="tech-name">{tech}</span>
              </div>
            ))}
          </div>

          {result.matched_categories && (
            <div style={{ marginTop: 20 }}>
              <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginRight: 8 }}>
                Matched categories:
              </span>
              <div className="tags" style={{ display: 'inline-flex' }}>
                {result.matched_categories.map(cat => (
                  <span key={cat} className="tag">{cat}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {!result && !loading && !error && (
        <div className="empty-state" style={{ marginTop: 40 }}>
          <div className="empty-icon">🧰</div>
          <p>Enter a project idea to get technology recommendations</p>
        </div>
      )}
    </div>
  );
}

export default TechRecommendations;
