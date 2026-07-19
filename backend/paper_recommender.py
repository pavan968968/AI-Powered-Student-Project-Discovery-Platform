"""
Paper Recommender - Fetches relevant research papers from Semantic Scholar API.
"""
import requests


SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"


def recommend_papers(query: str, limit: int = 5) -> dict:
    """
    Search for relevant research papers using Semantic Scholar API.
    Returns top papers with title, authors, year, abstract, and URL.
    """
    try:
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,abstract,url,citationCount",
        }

        response = requests.get(SEMANTIC_SCHOLAR_API, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            papers = []
            for paper in data.get("data", []):
                authors = [a.get("name", "Unknown") for a in paper.get("authors", [])]
                papers.append({
                    "title": paper.get("title", "Untitled"),
                    "authors": authors[:3],  # Limit to first 3 authors
                    "year": paper.get("year"),
                    "abstract": (paper.get("abstract") or "")[:300],
                    "url": paper.get("url", ""),
                    "citations": paper.get("citationCount", 0),
                })

            return {
                "query": query,
                "papers": papers,
                "source": "Semantic Scholar",
                "total_found": data.get("total", len(papers)),
            }

        elif response.status_code == 429:
            # Rate limited — try arXiv as fallback
            return _arxiv_fallback(query, limit)
        else:
            return _arxiv_fallback(query, limit)

    except Exception as e:
        return _arxiv_fallback(query, limit)


def _arxiv_fallback(query: str, limit: int = 5) -> dict:
    """Fallback to arXiv API if Semantic Scholar is unavailable."""
    try:
        import xml.etree.ElementTree as ET

        arxiv_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        response = requests.get(arxiv_url, params=params, timeout=10)

        if response.status_code == 200:
            root = ET.fromstring(response.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}

            papers = []
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns)
                summary = entry.find("atom:summary", ns)
                published = entry.find("atom:published", ns)
                link = entry.find("atom:id", ns)

                authors = []
                for author in entry.findall("atom:author", ns):
                    name = author.find("atom:name", ns)
                    if name is not None:
                        authors.append(name.text)

                papers.append({
                    "title": title.text.strip() if title is not None else "Untitled",
                    "authors": authors[:3],
                    "year": int(published.text[:4]) if published is not None else None,
                    "abstract": (summary.text.strip() if summary is not None else "")[:300],
                    "url": link.text if link is not None else "",
                    "citations": None,
                })

            return {
                "query": query,
                "papers": papers,
                "source": "arXiv",
                "total_found": len(papers),
            }

    except Exception:
        pass

    return {
        "query": query,
        "papers": [],
        "source": "unavailable",
        "error": "Both Semantic Scholar and arXiv APIs are unavailable. Please try again later.",
    }
