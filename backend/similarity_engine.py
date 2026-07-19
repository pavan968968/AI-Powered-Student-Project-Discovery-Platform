"""
Similarity Engine - Computes embeddings and finds similar projects using Sentence Transformers.
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Lazy-load the model to avoid slow startup
_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def compute_embedding(text: str) -> list:
    """Convert text into a dense vector embedding."""
    model = _get_model()
    embedding = model.encode(text, show_progress_bar=False)
    return embedding.tolist()


def compute_embeddings_batch(texts: list[str]) -> list[list]:
    """Compute embeddings for a batch of texts."""
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    return embeddings.tolist()


def find_similar_projects(query: str, projects: list, top_k: int = 5) -> list:
    """
    Find the most similar projects to a query text.
    Returns a list of dicts with project info and similarity score.
    """
    if not projects:
        return []

    query_embedding = np.array(compute_embedding(query)).reshape(1, -1)

    # Build project texts and embeddings
    project_texts = []
    valid_projects = []

    for p in projects:
        if p.get("embedding") and len(p["embedding"]) > 0:
            valid_projects.append(p)
        else:
            # Compute on the fly
            text = f"{p['title']}. {p['abstract']}"
            project_texts.append((p, text))

    # Compute missing embeddings
    if project_texts:
        texts = [t[1] for t in project_texts]
        embeddings = compute_embeddings_batch(texts)
        for (proj, _), emb in zip(project_texts, embeddings):
            proj["embedding"] = emb
            valid_projects.append(proj)

    if not valid_projects:
        return []

    # Compute similarities
    project_embeddings = np.array([p["embedding"] for p in valid_projects])
    similarities = cosine_similarity(query_embedding, project_embeddings)[0]

    # Rank and return top-k
    ranked_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in ranked_indices:
        proj = valid_projects[idx]
        results.append({
            "id": proj["id"],
            "title": proj["title"],
            "authors": proj["authors"],
            "year": proj["year"],
            "abstract": proj["abstract"],
            "domain": proj["domain"],
            "technologies": proj["technologies"],
            "similarity_score": round(float(similarities[idx]), 4)
        })

    return results
