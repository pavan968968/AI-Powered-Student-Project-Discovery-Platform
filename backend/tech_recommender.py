"""
Technology Recommender - Suggests technologies for a project idea using Grok LLM or keyword matching.
"""
import json
import re
from pathlib import Path

# ── xAI Grok API Key ──
XAI_API_KEY = "xai-yQ12gxd95LTt2TSRWYAB4vWjcx1lfvxa6aYyBVtCgG7simmMsT0YPBagnLdOxauNarqGHwiNp2s9SEi9"
XAI_BASE_URL = "https://api.x.ai/v1"

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_tech_db() -> dict:
    """Load the technology knowledge base."""
    tech_file = _DATA_DIR / "technologies.json"
    with open(tech_file, "r", encoding="utf-8") as f:
        return json.load(f)


def _keyword_based_recommendations(idea: str) -> dict:
    """Recommend technologies using keyword matching."""
    tech_db = _load_tech_db()
    idea_lower = idea.lower()

    recommended = set()
    matched_categories = []

    # Check technology keywords
    for keyword, techs in tech_db.get("technology_keywords", {}).items():
        if keyword in idea_lower:
            recommended.update(techs)
            matched_categories.append(keyword)

    # Check domain-specific technologies
    for domain, categories in tech_db.get("domains", {}).items():
        domain_lower = domain.lower()
        # Check if domain name matches
        if any(word in idea_lower for word in domain_lower.split()):
            for category_name, techs in categories.items():
                recommended.update(techs)
            matched_categories.append(domain)

    if not recommended:
        # Default recommendations for unmatched queries
        recommended = {"Python", "React", "FastAPI", "Docker", "PostgreSQL", "Git"}
        matched_categories = ["general"]

    return {
        "idea": idea,
        "technologies": sorted(list(recommended))[:12],
        "matched_categories": matched_categories,
        "method": "keyword-based",
    }


def _grok_tech_recommendations(idea: str) -> dict:
    """Recommend technologies using xAI Grok API."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)

        prompt = f"""You are a senior software architect advising a student on their project.

Given the following project idea, recommend 8-12 specific technologies, frameworks, libraries, and tools they should use to build it.

Project idea: {idea}

Provide recommendations as a JSON array of strings. Only output the JSON array, nothing else.
Example: ["Python", "TensorFlow", "React", "FastAPI"]"""

        response = client.chat.completions.create(
            model="grok-3-mini-fast",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content.strip()

        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            technologies = json.loads(match.group())
        else:
            technologies = [line.strip("- •").strip() for line in content.split("\n") if line.strip()]

        return {
            "idea": idea,
            "technologies": technologies[:12],
            "method": "llm",
        }

    except Exception as e:
        result = _keyword_based_recommendations(idea)
        result["llm_error"] = str(e)
        return result


def recommend_technologies(idea: str) -> dict:
    """Recommend technologies for a project idea."""
    if XAI_API_KEY:
        return _grok_tech_recommendations(idea)
    else:
        return _keyword_based_recommendations(idea)
