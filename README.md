# 🧠 Project Ahaa

**AI-Powered Student Project Discovery Platform**

Project Ahaa captures student project ideas and helps future students discover existing projects, avoid duplication, and improve ideas using modern AI techniques.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **AI Similarity Search** | Find similar projects using Sentence Transformer embeddings and cosine similarity |
| 💡 **Idea Improver** | Get AI-generated improvement suggestions (LLM or rule-based fallback) |
| 🕸️ **Knowledge Graph** | Interactive Cytoscape.js visualization of projects, technologies, and domains |
| 📅 **Idea Timeline** | See how project ideas evolved over the years |
| 📄 **Paper Recommendations** | Discover relevant research papers from Semantic Scholar / arXiv |
| ⚙️ **Tech Recommendations** | Get technology stack suggestions for your project idea |

---

## 🏗️ Tech Stack

- **Frontend**: React.js, Cytoscape.js, Axios
- **Backend**: Python, FastAPI, Uvicorn
- **AI**: Sentence Transformers (`all-MiniLM-L6-v2`), OpenAI API (optional)
- **Graph**: NetworkX
- **Data**: JSON files (no database)
- **External APIs**: Semantic Scholar, arXiv

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm

### Backend Setup

```bash
cd project-ahaa/backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# (Optional) Set OpenAI API key for LLM-based features
set OPENAI_API_KEY=your_key_here       # Windows
# export OPENAI_API_KEY=your_key_here  # Mac/Linux

# Start the server
uvicorn main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**

> **Note**: On first request involving embeddings, the system downloads the Sentence Transformers model (~80MB). This is a one-time download.

### Frontend Setup

```bash
cd project-ahaa/frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at **http://localhost:3000**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/projects` | List all projects |
| POST | `/projects` | Add a new project |
| POST | `/similar-projects` | Find similar projects |
| POST | `/idea-improvement` | Get improvement suggestions |
| POST | `/technology-recommendations` | Get tech stack suggestions |
| POST | `/research-papers` | Find research papers |
| GET | `/knowledge-graph` | Get graph visualization data |
| GET | `/timeline/{project_id}` | Get idea evolution timeline |

---

## 📂 Project Structure

```
project-ahaa/
├── backend/
│   ├── main.py                 # FastAPI app & endpoints
│   ├── similarity_engine.py    # Embedding & cosine similarity
│   ├── idea_improver.py        # LLM / rule-based improvements
│   ├── tech_recommender.py     # Technology suggestions
│   ├── paper_recommender.py    # Semantic Scholar / arXiv
│   ├── timeline_engine.py      # Idea evolution timeline
│   ├── knowledge_graph.py      # NetworkX graph builder
│   └── requirements.txt
├── data/
│   ├── projects.json           # 30 sample student projects
│   └── technologies.json       # Technology knowledge base
├── frontend/
│   ├── public/index.html
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── index.css
│       └── components/
│           ├── ProjectSearch.js
│           ├── ProjectGraph.js
│           ├── IdeaImprover.js
│           ├── ProjectTimeline.js
│           ├── PaperRecommendations.js
│           └── TechRecommendations.js
└── README.md
```

---

## 📊 Sample Dataset

The system includes **30 sample student projects** across 9 domains:

- Artificial Intelligence
- Healthcare
- Agriculture
- IoT
- Renewable Energy
- Cybersecurity
- Education Technology
- Computer Vision
- Natural Language Processing

---

## 🔑 Notes

- **Without OpenAI API key**: The Idea Improver and Tech Recommender use smart rule-based fallback systems that work without any API key.
- **With OpenAI API key**: Set the `OPENAI_API_KEY` environment variable to enable LLM-powered suggestions.
- **Embeddings**: Sentence Transformers runs locally — no API key needed.
