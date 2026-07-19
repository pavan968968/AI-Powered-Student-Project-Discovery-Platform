"""
Timeline Engine - Shows how project ideas evolve over time by grouping similar projects.
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from similarity_engine import compute_embedding


def get_timeline(project_id: int, projects: list, similarity_threshold: float = 0.45) -> dict:
    """
    Build an idea evolution timeline for a given project.
    Groups similar projects and sorts by year to show how the idea evolved.
    """
    # Find the target project
    target = None
    for p in projects:
        if p["id"] == project_id:
            target = p
            break

    if target is None:
        return {"error": f"Project {project_id} not found", "timeline": []}

    # Ensure target has embedding
    if not target.get("embedding") or len(target["embedding"]) == 0:
        target["embedding"] = compute_embedding(f"{target['title']}. {target['abstract']}")

    target_embedding = np.array(target["embedding"]).reshape(1, -1)

    # Compute embeddings for all projects
    timeline_projects = []
    for p in projects:
        if not p.get("embedding") or len(p["embedding"]) == 0:
            p["embedding"] = compute_embedding(f"{p['title']}. {p['abstract']}")

        emb = np.array(p["embedding"]).reshape(1, -1)
        sim = cosine_similarity(target_embedding, emb)[0][0]

        if sim >= similarity_threshold:
            timeline_projects.append({
                "id": p["id"],
                "title": p["title"],
                "authors": p["authors"],
                "year": p["year"],
                "abstract": p["abstract"],
                "domain": p["domain"],
                "technologies": p["technologies"],
                "similarity_score": round(float(sim), 4),
                "is_target": p["id"] == project_id,
            })

    # Sort by year
    timeline_projects.sort(key=lambda x: (x["year"], -x["similarity_score"]))

    return {
        "project_id": project_id,
        "project_title": target["title"],
        "timeline": timeline_projects,
        "total_related": len(timeline_projects),
    }
