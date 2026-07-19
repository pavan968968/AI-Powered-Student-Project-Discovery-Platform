import React, { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';
import coseBilkent from 'cytoscape-cose-bilkent';
import axios from 'axios';

cytoscape.use(coseBilkent);

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const NODE_STYLES = {
  project: { color: '#6366f1', shape: 'ellipse', size: 30 },
  technology: { color: '#34d399', shape: 'round-rectangle', size: 22 },
  domain: { color: '#f59e0b', shape: 'diamond', size: 28 },
};

function ProjectGraph() {
  const containerRef = useRef(null);
  const cyRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const res = await axios.get(`${API}/knowledge-graph`);
        const data = res.data;

        const projectCount = data.nodes.filter(n => n.data.type === 'project').length;
        const techCount = data.nodes.filter(n => n.data.type === 'technology').length;
        const domainCount = data.nodes.filter(n => n.data.type === 'domain').length;
        setStats({ projects: projectCount, techs: techCount, domains: domainCount, edges: data.edges.length });

        if (cyRef.current) {
          cyRef.current.destroy();
        }

        cyRef.current = cytoscape({
          container: containerRef.current,
          elements: {
            nodes: data.nodes.map(n => ({
              data: {
                ...n.data,
                bgColor: NODE_STYLES[n.data.type]?.color || '#6366f1',
                nodeSize: NODE_STYLES[n.data.type]?.size || 24,
                nodeShape: NODE_STYLES[n.data.type]?.shape || 'ellipse',
              },
            })),
            edges: data.edges.map(e => ({
              data: { ...e.data },
            })),
          },
          style: [
            {
              selector: 'node',
              style: {
                'background-color': 'data(bgColor)',
                'label': 'data(label)',
                'color': '#e8e8f0',
                'text-valign': 'bottom',
                'text-halign': 'center',
                'font-size': '8px',
                'font-family': 'Inter, sans-serif',
                'text-margin-y': 6,
                'width': 'data(nodeSize)',
                'height': 'data(nodeSize)',
                'shape': 'data(nodeShape)',
                'border-width': 2,
                'border-color': 'data(bgColor)',
                'border-opacity': 0.5,
                'text-max-width': '80px',
                'text-wrap': 'ellipsis',
                'overlay-opacity': 0,
              },
            },
            {
              selector: 'edge',
              style: {
                'width': 1,
                'line-color': 'rgba(255, 255, 255, 0.1)',
                'curve-style': 'bezier',
                'opacity': 0.6,
              },
            },
            {
              selector: 'edge[relationship = "SIMILAR_TO"]',
              style: {
                'line-color': 'rgba(99, 102, 241, 0.3)',
                'line-style': 'dashed',
                'width': 1.5,
              },
            },
            {
              selector: 'edge[relationship = "USES_TECH"]',
              style: {
                'line-color': 'rgba(52, 211, 153, 0.25)',
              },
            },
            {
              selector: 'edge[relationship = "BELONGS_TO"]',
              style: {
                'line-color': 'rgba(245, 158, 11, 0.3)',
              },
            },
            {
              selector: 'node:active',
              style: {
                'overlay-opacity': 0,
              },
            },
          ],
          layout: {
            name: 'cose-bilkent',
            animate: false,
            randomize: true,
            idealEdgeLength: 120,
            nodeRepulsion: 8000,
            edgeElasticity: 0.15,
            nestingFactor: 0.1,
            gravity: 0.3,
            numIter: 2500,
            tile: true,
            fit: true,
            padding: 30,
          },
          minZoom: 0.3,
          maxZoom: 3,
          wheelSensitivity: 0.3,
        });

        // Hover interaction
        cyRef.current.on('mouseover', 'node', (e) => {
          const node = e.target;
          node.style({
            'border-width': 3,
            'border-opacity': 1,
            'font-size': '10px',
            'text-max-width': '200px',
            'text-wrap': 'wrap',
            'z-index': 999,
          });
          node.connectedEdges().style({ 'opacity': 1, 'width': 2 });
        });

        cyRef.current.on('mouseout', 'node', (e) => {
          const node = e.target;
          node.style({
            'border-width': 2,
            'border-opacity': 0.5,
            'font-size': '8px',
            'text-max-width': '80px',
            'text-wrap': 'ellipsis',
            'z-index': 0,
          });
          node.connectedEdges().style({ 'opacity': 0.6, 'width': 1 });
        });

        setLoading(false);
      } catch (err) {
        setError('Failed to load knowledge graph. Make sure the backend is running.');
        setLoading(false);
      }
    };

    fetchGraph();

    return () => {
      if (cyRef.current) cyRef.current.destroy();
    };
  }, []);

  return (
    <div className="card">
      <h2 className="card-title">🕸️ Project Knowledge Graph</h2>
      <p className="card-subtitle">
        Interactive visualization of projects, technologies, and domains
      </p>

      {error && <div className="error-msg">{error}</div>}

      {loading && !error && (
        <div className="loading">
          <div className="spinner"></div>
          <span>Building knowledge graph (computing embeddings)...</span>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>This may take a moment on first load</span>
        </div>
      )}

      <div
        className="graph-container"
        ref={containerRef}
        style={{ display: loading || error ? 'none' : 'block' }}
      />

      {stats && !loading && (
        <div className="graph-legend">
          <div className="legend-item">
            <span className="legend-dot project"></span>
            Projects ({stats.projects})
          </div>
          <div className="legend-item">
            <span className="legend-dot technology"></span>
            Technologies ({stats.techs})
          </div>
          <div className="legend-item">
            <span className="legend-dot domain"></span>
            Domains ({stats.domains})
          </div>
          <div className="legend-item" style={{ marginLeft: 'auto', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
            {stats.edges} connections • Scroll to zoom • Drag to pan
          </div>
        </div>
      )}
    </div>
  );
}

export default ProjectGraph;
