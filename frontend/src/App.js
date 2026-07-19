import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ProjectSearch from './components/ProjectSearch';
import ProjectGraph from './components/ProjectGraph';
import IdeaImprover from './components/IdeaImprover';
import ProjectTimeline from './components/ProjectTimeline';
import PaperRecommendations from './components/PaperRecommendations';
import TechRecommendations from './components/TechRecommendations';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const TABS = [
  { id: 'search', label: 'Search', icon: '🔍' },
  { id: 'improve', label: 'Idea Improver', icon: '💡' },
  { id: 'graph', label: 'Knowledge Graph', icon: '🕸️' },
  { id: 'timeline', label: 'Timeline', icon: '📅' },
  { id: 'papers', label: 'Papers', icon: '📄' },
  { id: 'tech', label: 'Tech Stack', icon: '⚙️' },
];

function App() {
  const [activeTab, setActiveTab] = useState('search');
  const [apiStatus, setApiStatus] = useState(null);
  const [statusLoading, setStatusLoading] = useState(true);

  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    setStatusLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api-status`, { timeout: 30000 });
      setApiStatus(response.data);
    } catch (err) {
      setApiStatus({ backend_down: true, error: err.message });
    }
    setStatusLoading(false);
  };

  const renderTab = () => {
    switch (activeTab) {
      case 'search': return <ProjectSearch />;
      case 'improve': return <IdeaImprover />;
      case 'graph': return <ProjectGraph />;
      case 'timeline': return <ProjectTimeline />;
      case 'papers': return <PaperRecommendations />;
      case 'tech': return <TechRecommendations />;
      default: return <ProjectSearch />;
    }
  };

  const getFriendlyError = (error) => {
    if (!error) return null;
    if (error.includes('429') || error.toLowerCase().includes('quota')) return 'API quota exceeded — resets daily';
    if (error.includes('403') || error.toLowerCase().includes('permission')) return 'Invalid API key';
    if (error.includes('401') || error.toLowerCase().includes('unauthorized')) return 'API key unauthorized';
    if (error.toLowerCase().includes('timeout') || error.toLowerCase().includes('timed out')) return 'API request timed out';
    if (error.toLowerCase().includes('network') || error.toLowerCase().includes('connection')) return 'Network error';
    return 'API error — check console';
  };

  const renderStatusBadge = () => {
    if (statusLoading) {
      return <span className="status-badge status-checking">⏳ Checking API...</span>;
    }
    if (!apiStatus || apiStatus.backend_down) {
      return <span className="status-badge status-down">🔴 Backend Offline</span>;
    }
    const friendlyError = getFriendlyError(apiStatus.gemini_error);
    return (
      <div className="status-badges">
        <span className={`status-badge ${apiStatus.gemini_api_working ? 'status-ok' : 'status-warn'}`}>
          {apiStatus.gemini_api_working ? '🟢 Gemini AI Active' : '🟡 Gemini: Fallback Mode'}
        </span>
        <span className={`status-badge ${apiStatus.similarity_engine ? 'status-ok' : 'status-down'}`}>
          {apiStatus.similarity_engine ? '🟢 Embeddings Ready' : '🔴 Embeddings Error'}
        </span>
        {friendlyError && (
          <span className="status-badge status-detail" title={apiStatus.gemini_error}>
            ⚠️ {friendlyError}
          </span>
        )}
        <button className="status-refresh" onClick={checkApiStatus} title="Refresh status">🔄</button>
      </div>
    );
  };

  return (
    <div className="app">
      <header className="header">
        <h1 className="header-title">ProjectDNA</h1>
        <p className="header-subtitle">
          AI-Powered Student Project Discovery Platform
        </p>
        <div className="api-status-bar">
          {renderStatusBadge()}
        </div>
      </header>

      <nav className="nav">
        {TABS.map(tab => (
          <button
            key={tab.id}
            className={`nav-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="nav-icon">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </nav>

      <main>{renderTab()}</main>
    </div>
  );
}

export default App;
