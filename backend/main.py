"""
ProjectDNA - FastAPI Backend
AI-powered student project discovery platform.
"""
import json
import sys
import traceback
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── xAI Grok API Key ──
XAI_API_KEY = "xai-yQ12gxd95LTt2TSRWYAB4vWjcx1lfvxa6aYyBVtCgG7simmMsT0YPBagnLdOxauNarqGHwiNp2s9SEi9"
XAI_BASE_URL = "https://api.x.ai/v1"

# ── Data paths ──
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROJECTS_FILE = DATA_DIR / "projects.json"

# ── FastAPI App ──
app = FastAPI(
    title="ProjectDNA",
    description="AI-powered student project discovery platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ──

def load_projects() -> list:
    """Load projects from JSON file."""
    if not PROJECTS_FILE.exists():
        return []
    with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_projects(projects: list):
    """Save projects to JSON file."""
    with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)


# ── Pydantic Models ──

class ProjectCreate(BaseModel):
    title: str
    authors: list[str]
    year: int
    abstract: str
    domain: str
    technologies: list[str] = []
    keywords: list[str] = []


class QueryInput(BaseModel):
    query: str


class SimilarProjectsInput(BaseModel):
    query: str
    top_k: int = 5


# ── Endpoints ──

@app.get("/")
def root():
    return {"message": "Welcome to ProjectDNA API", "version": "1.0.0"}


@app.get("/api-status")
def api_status():
    """Check if the xAI Grok API is working."""
    status = {
        "gemini_key_configured": bool(XAI_API_KEY),
        "gemini_api_working": False,
        "gemini_model": None,
        "gemini_error": None,
        "similarity_engine": False,
        "similarity_error": None,
    }

    # Test xAI Grok API
    if XAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)
            response = client.chat.completions.create(
                model="grok-3-mini-fast",
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5,
            )
            if response and response.choices[0].message.content:
                status["gemini_api_working"] = True
                status["gemini_model"] = "grok-3-mini-fast"
        except Exception as e:
            status["gemini_error"] = str(e)

    # Test Similarity Engine
    try:
        from similarity_engine import SimilarityEngine
        engine = SimilarityEngine()
        status["similarity_engine"] = True
    except Exception as e:
        # Try alternate import
        try:
            from similarity_engine import find_similar_projects
            status["similarity_engine"] = True
        except Exception as e2:
            status["similarity_error"] = str(e2)

    return status


@app.get("/projects")
def get_projects():
    """Return all projects."""
    projects = load_projects()
    # Return projects without embeddings for cleaner response
    return [
        {k: v for k, v in p.items() if k != "embedding"}
        for p in projects
    ]


@app.post("/projects")
def add_project(project: ProjectCreate):
    """Add a new project."""
    projects = load_projects()
    new_id = max((p["id"] for p in projects), default=0) + 1
    new_project = {
        "id": new_id,
        "title": project.title,
        "authors": project.authors,
        "year": project.year,
        "abstract": project.abstract,
        "domain": project.domain,
        "technologies": project.technologies,
        "keywords": project.keywords,
        "embedding": [],
    }
    projects.append(new_project)
    save_projects(projects)
    return {"message": "Project added successfully", "project": {k: v for k, v in new_project.items() if k != "embedding"}}


@app.post("/similar-projects")
def similar_projects(input: SimilarProjectsInput):
    """Find similar projects using AI embeddings."""
    from similarity_engine import find_similar_projects

    projects = load_projects()
    results = find_similar_projects(input.query, projects, top_k=input.top_k)

    # Save updated embeddings
    save_projects(projects)

    return {"query": input.query, "results": results}


@app.post("/idea-improvement")
def idea_improvement(input: QueryInput):
    """Get AI-generated improvement suggestions."""
    from idea_improver import improve_idea

    result = improve_idea(input.query)
    return result


@app.post("/technology-recommendations")
def technology_recommendations(input: QueryInput):
    """Get technology recommendations for a project idea."""
    from tech_recommender import recommend_technologies

    result = recommend_technologies(input.query)
    return result


@app.post("/research-papers")
def research_papers(input: QueryInput):
    """Get research paper recommendations."""
    from paper_recommender import recommend_papers

    result = recommend_papers(input.query)
    return result


@app.get("/knowledge-graph")
def knowledge_graph():
    """Get knowledge graph data for visualization."""
    from knowledge_graph import build_knowledge_graph

    projects = load_projects()
    graph_data = build_knowledge_graph(projects)

    # Save updated embeddings
    save_projects(projects)

    return graph_data


@app.get("/timeline/{project_id}")
def timeline(project_id: int):
    """Get idea evolution timeline for a project."""
    from timeline_engine import get_timeline

    projects = load_projects()
    result = get_timeline(project_id, projects)

    # Save updated embeddings
    save_projects(projects)

    if "error" in result and not result.get("timeline"):
        raise HTTPException(status_code=404, detail=result["error"])

    return result
