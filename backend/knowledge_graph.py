"""
Knowledge Graph - Builds a project knowledge graph using NetworkX.
"""
import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from similarity_engine import compute_embedding


def build_knowledge_graph(projects: list, similarity_threshold: float = 0.5) -> dict:
    """
    Build a knowledge graph connecting projects, technologies, and domains.

    Node types: project, technology, domain
    Edge types: USES_TECH, BELONGS_TO, SIMILAR_TO
    """
    G = nx.Graph()

    # ── Add project nodes ──
    for p in projects:
        G.add_node(
            f"project_{p['id']}",
            label=p["title"],
            type="project",
            year=p["year"],
            domain=p["domain"],
        )

    # ── Add technology nodes and USES_TECH edges ──
    tech_set = set()
    for p in projects:
        for tech in p.get("technologies", []):
            tech_id = f"tech_{tech.replace(' ', '_')}"
            if tech not in tech_set:
                G.add_node(tech_id, label=tech, type="technology")
                tech_set.add(tech)
            G.add_edge(f"project_{p['id']}", tech_id, relationship="USES_TECH")

    # ── Add domain nodes and BELONGS_TO edges ──
    domain_set = set()
    for p in projects:
        domain = p.get("domain", "Unknown")
        domain_id = f"domain_{domain.replace(' ', '_')}"
        if domain not in domain_set:
            G.add_node(domain_id, label=domain, type="domain")
            domain_set.add(domain)
        G.add_edge(f"project_{p['id']}", domain_id, relationship="BELONGS_TO")

    # ── Add SIMILAR_TO edges ──
    # Compute embeddings for all projects
    valid_projects = []
    for p in projects:
        emb = p.get("embedding")
        if isinstance(emb, list) and len(emb) > 0:
            valid_projects.append(p)
            continue
        p["embedding"] = compute_embedding(f"{p['title']}. {p['abstract']}")
        valid_projects.append(p)

    embeddings = np.array([p["embedding"] for p in valid_projects])
    sim_matrix = cosine_similarity(embeddings)

    for i in range(len(valid_projects)):
        for j in range(i + 1, len(valid_projects)):
            if sim_matrix[i][j] >= similarity_threshold:
                G.add_edge(
                    f"project_{valid_projects[i]['id']}",
                    f"project_{valid_projects[j]['id']}",
                    relationship="SIMILAR_TO",
                    weight=round(float(sim_matrix[i][j]), 4),
                )

    return _graph_to_cytoscape(G)


def _graph_to_cytoscape(G: nx.Graph) -> dict:
    """Convert NetworkX graph to Cytoscape.js compatible format."""
    nodes = []
    for node_id, attrs in G.nodes(data=True):
        nodes.append({
            "data": {
                "id": node_id,
                "label": attrs.get("label", node_id),
                "type": attrs.get("type", "unknown"),
                **{k: v for k, v in attrs.items() if k not in ("label", "type")},
            }
        })

    edges = []
    for source, target, attrs in G.edges(data=True):
        edges.append({
            "data": {
                "id": f"{source}-{target}",
                "source": source,
                "target": target,
                "relationship": attrs.get("relationship", "RELATED"),
                **{k: v for k, v in attrs.items() if k != "relationship"},
            }
        })

    return {"nodes": nodes, "edges": edges}
