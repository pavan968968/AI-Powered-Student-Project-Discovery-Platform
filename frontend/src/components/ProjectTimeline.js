import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function ProjectTimeline() {
  const [projects, setProjects] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [timeline, setTimeline] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingList, setLoadingList] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const res = await axios.get(`${API}/projects`);
        setProjects(res.data);
      } catch (err) {
        setError('Failed to load projects.');
      }
      setLoadingList(false);
    };
    fetchProjects();
  }, []);

  const handleSelect = async (id) => {
    if (!id) return;
    setSelectedId(id);
    setLoading(true);
    setError('');
    setTimeline(null);
    try {
      const res = await axios.get(`${API}/timeline/${id}`);
      setTimeline(res.data);
    } catch (err) {
      setError('Failed to load timeline.');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2 className="card-title">📅 Idea Evolution Timeline</h2>
      <p className="card-subtitle">
        See how project ideas evolved over the years by selecting a project
      </p>

      {loadingList ? (
        <div className="loading">
          <div className="spinner"></div>
          <span>Loading projects...</span>
        </div>
      ) : (
        <select
          id="timeline-select"
          className="project-select"
          value={selectedId}
          onChange={(e) => handleSelect(e.target.value)}
        >
          <option value="">Select a project to view its evolution...</option>
          {projects.map(p => (
            <option key={p.id} value={p.id}>
              {p.title} ({p.year})
            </option>
          ))}
        </select>
      )}

      {error && <div className="error-msg" style={{ marginTop: 16 }}>{error}</div>}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <span>Computing similarity and building timeline...</span>
        </div>
      )}

      {timeline && !loading && (
        <div>
          <div className="section-header" style={{ marginTop: 24 }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 600 }}>
              Evolution of: {timeline.project_title}
            </h3>
            <span className="section-count">
              {timeline.total_related} related project{timeline.total_related !== 1 ? 's' : ''}
            </span>
          </div>

          {timeline.timeline.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🔭</div>
              <p>No related projects found in the timeline.</p>
            </div>
          ) : (
            <div className="timeline">
              {timeline.timeline.map((item, i) => (
                <div
                  key={item.id}
                  className={`timeline-item ${item.is_target ? 'target' : ''}`}
                  style={{ animationDelay: `${i * 0.1}s` }}
                >
                  <span className="timeline-year">{item.year}</span>
                  <div className="timeline-title">
                    {item.title}
                    {item.is_target && <span style={{ color: 'var(--accent-secondary)', marginLeft: 8, fontSize: '0.8rem' }}>← Selected</span>}
                  </div>
                  <p className="timeline-abstract">{item.abstract}</p>
                  <div style={{ display: 'flex', gap: 8, marginTop: 8, alignItems: 'center' }}>
                    <span className="similarity-badge" style={{ fontSize: '0.72rem' }}>
                      {(item.similarity_score * 100).toFixed(1)}% match
                    </span>
                    <span className="tag domain">{item.domain}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!timeline && !loading && !error && !loadingList && (
        <div className="empty-state" style={{ marginTop: 40 }}>
          <div className="empty-icon">⏳</div>
          <p>Select a project above to see how its idea evolved over time</p>
        </div>
      )}
    </div>
  );
}

export default ProjectTimeline;
