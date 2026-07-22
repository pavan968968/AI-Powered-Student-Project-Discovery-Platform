"""
Idea Improver - Suggests improvements for project ideas using Grok LLM or rule-based fallback.
"""
import json
import os
import re

# ── xAI Grok API Key ──
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
XAI_BASE_URL = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")

# ── Rule-based fallback improvements ──
_IMPROVEMENT_TEMPLATES = {
    "general": [
        "Add a user-friendly web dashboard for visualization and monitoring",
        "Implement a REST API for third-party integrations",
        "Add data export functionality (CSV, PDF reports)",
        "Include role-based access control for multiple user types",
        "Add real-time notifications and alerts via email or SMS",
        "Implement logging and analytics to track system usage",
    ],
    "ai": [
        "Use transfer learning to improve model accuracy with less training data",
        "Add model explainability using SHAP or LIME",
        "Implement A/B testing to compare different model versions",
        "Add an automated retraining pipeline for continuous improvement",
        "Integrate edge AI deployment for low-latency inference",
        "Use ensemble methods to combine multiple model predictions",
    ],
    "iot": [
        "Add edge computing for local data processing and reduced latency",
        "Implement OTA (over-the-air) firmware updates",
        "Add battery monitoring and power optimization",
        "Use LoRa or NB-IoT for long-range, low-power connectivity",
        "Implement redundant sensor arrays for fault tolerance",
        "Add predictive maintenance using sensor data trends",
    ],
    "mobile": [
        "Add offline mode with local data synchronization",
        "Implement push notifications for real-time updates",
        "Add biometric authentication (fingerprint, face ID)",
        "Optimize for low-bandwidth environments",
        "Add multi-language support for wider accessibility",
    ],
    "web": [
        "Implement Progressive Web App (PWA) for offline access",
        "Add real-time collaboration features using WebSocket",
        "Implement server-side rendering for better SEO and performance",
        "Add OAuth integration for social login",
        "Implement caching strategies for improved load times",
    ],
    "security": [
        "Add end-to-end encryption for sensitive data",
        "Implement rate limiting and DDoS protection",
        "Add audit logging for compliance and traceability",
        "Use zero-trust architecture principles",
        "Implement automated vulnerability scanning",
    ],
}

_KEYWORD_CATEGORY_MAP = {
    "ai": ["machine learning", "deep learning", "neural", "cnn", "lstm", "bert", "gpt",
           "classification", "prediction", "detection", "recognition", "nlp", "computer vision",
           "model", "training", "inference", "embedding"],
    "iot": ["iot", "sensor", "arduino", "raspberry", "esp32", "mqtt", "smart home",
            "monitoring", "automation", "edge"],
    "mobile": ["mobile", "android", "ios", "app", "flutter", "react native"],
    "web": ["web", "website", "dashboard", "portal", "react", "frontend", "backend", "api"],
    "security": ["security", "cyber", "encryption", "malware", "intrusion", "phishing",
                 "authentication", "privacy"],
}


def _detect_categories(text: str) -> list[str]:
    """Detect relevant categories from the idea text."""
    text_lower = text.lower()
    categories = []
    for cat, keywords in _KEYWORD_CATEGORY_MAP.items():
        if any(kw in text_lower for kw in keywords):
            categories.append(cat)
    if not categories:
        categories = ["general"]
    return categories


def _rule_based_improvements(idea: str) -> dict:
    """Generate improvements using keyword matching and templates."""
    categories = _detect_categories(idea)

    improvements = []
    for cat in categories:
        improvements.extend(_IMPROVEMENT_TEMPLATES.get(cat, []))
    # Always add some general improvements
    improvements.extend(_IMPROVEMENT_TEMPLATES["general"][:3])

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for imp in improvements:
        if imp not in seen:
            seen.add(imp)
            unique.append(imp)

    return {
        "idea": idea,
        "improvements": unique[:8],
        "categories_detected": categories,
        "method": "rule-based",
    }


def _grok_improvements(idea: str) -> dict:
    """Generate improvements using xAI Grok API."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)

        prompt = f"""You are an expert academic advisor helping students improve their project ideas.

Given the following student project idea, suggest 6-8 specific, actionable improvements and extensions.

Project idea: {idea}

Provide improvements as a JSON array of strings. Only output the JSON array, nothing else.
Example: ["improvement 1", "improvement 2"]"""

        response = client.chat.completions.create(
            model="grok-3-mini-fast",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content.strip()

        # Extract JSON array from response
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            improvements = json.loads(match.group())
        else:
            improvements = [line.strip("- •").strip() for line in content.split("\n") if line.strip()]

        return {
            "idea": idea,
            "improvements": improvements[:8],
            "method": "llm",
        }

    except Exception as e:
        # Fallback to rule-based if LLM fails
        result = _rule_based_improvements(idea)
        result["llm_error"] = str(e)
        return result


def improve_idea(idea: str) -> dict:
    """Generate improvement suggestions for a project idea."""
    if XAI_API_KEY:
        return _grok_improvements(idea)
    else:
        return _rule_based_improvements(idea)
