import importlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class KnowledgeGraphTests(unittest.TestCase):
    def test_build_knowledge_graph_creates_nodes_and_edges(self):
        kg = importlib.import_module("backend.knowledge_graph")

        def fake_embedding(text):
            return [0.1, 0.2, 0.3]

        kg.compute_embedding = fake_embedding

        projects = [
            {
                "id": 1,
                "title": "AI Study Planner",
                "abstract": "A smart planner for students.",
                "year": 2024,
                "domain": "Education",
                "technologies": ["Python", "React"],
            },
            {
                "id": 2,
                "title": "ML Resume Analyzer",
                "abstract": "A resume analyzer using machine learning.",
                "year": 2025,
                "domain": "Education",
                "technologies": ["Python", "FastAPI"],
            },
        ]

        result = kg.build_knowledge_graph(projects, similarity_threshold=0.0)

        self.assertTrue(result["nodes"], "Expected graph nodes to be created")
        self.assertTrue(result["edges"], "Expected graph edges to be created")
        self.assertTrue(any(node["data"]["type"] == "project" for node in result["nodes"]))
        self.assertTrue(any(node["data"]["type"] == "technology" for node in result["nodes"]))


if __name__ == "__main__":
    unittest.main()
