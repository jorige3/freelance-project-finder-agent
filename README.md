# 🚀 Freelance Project Finder AI Agent

An intelligent AI-powered application that automatically collects, scores, and recommends **quality freelance and remote opportunities** with a focus on **free-to-apply developer gigs**. Built with smart filtering, explainable AI scoring, and actionable proposals.

**Version:** 0.2.0  
**Status:** Active Development

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [Author](#author)

---

## 🎯 Overview

**Freelance Project Finder** is an AI agent designed to help developers efficiently discover relevant freelance opportunities. Instead of manually browsing job boards, this system:

1. **Collects** opportunities from multiple sources (RemoteOK, mock collectors)
2. **Intelligently Scores** projects based on skill relevance, difficulty level, and job type
3. **Filters** for tech-relevant roles and free-to-apply positions
4. **Generates** personalized proposals automatically
5. **Explains** scoring logic with transparent reasoning
6. **Recommends** the best opportunities via REST API or dashboard

---

## ✨ Features

### Core Features
- ✅ **Live Opportunity Collection** - Fetches freelance gigs from RemoteOK and other sources
- ✅ **AI-Powered Scoring Engine** - Ranks projects based on 17+ skill weights and difficulty factors
- ✅ **Smart Filtering** 
  - Only recommends tech/development roles to developers
  - Filters for free-to-apply opportunities
  - Minimum score threshold filtering (50+)
- ✅ **Explainable Scoring** - Shows detailed reasoning for each project score
- ✅ **Intelligent Proposals** - Generates contextual proposals or politely declines non-tech roles
- ✅ **RESTful API** - Full-featured FastAPI backend with multiple endpoints
- ✅ **Interactive Dashboard** - Streamlit-based UI for browsing and exploring opportunities
- ✅ **SQLite Database** - Persistent storage with efficient queries

### Recent Improvements
- 🔧 Consistent keyword matching with word boundaries across all scoring
- 🔧 Job-type detection to separate tech from non-tech roles
- 🔧 Personalized proposals (tech-focused for developers, decline templates for non-tech)
- 🔧 Minimum score threshold to reduce low-relevance recommendations
- 🔧 Improved negative keyword handling for senior/lead positions

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend API** | FastAPI 0.139+ |
| **Runtime** | Python 3.11+ |
| **Database** | SQLite with SQLAlchemy ORM |
| **Frontend** | Streamlit 1.59+ |
| **Data Processing** | Pandas 3.0+ |
| **Scraping** | BeautifulSoup4, HTTPX |
| **Web Server** | Uvicorn 0.50+ |
| **Validation** | Pydantic 2.13+ |

---

## 🏗️ Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Server                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Coordinator  │  │   Ranking    │  │   Proposal   │      │
│  │   Agent      │→→│   Engine     │→→│  Generator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                                                     │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  Collector   │→→│   Filter     │                         │
│  │   Manager    │  │   Agent      │                         │
│  └──────────────┘  └──────────────┘                         │
│         ↓                                                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │            SQLite Database                              ││
│  │    (freelance_projects table)                           ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
         ↓
    RemoteOK API / Collectors
```

### Agent Workflow

1. **CollectorAgent** - Fetches projects from external sources
2. **FilterAgent** - Applies free-to-apply filter and relevance filters
3. **RankingAgent** - Calculates and explains project scores
4. **ProposalAgent** - Generates contextual cover letters
5. **CoordinatorAgent** - Orchestrates all agents and returns results

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip

### Clone & Setup

```bash
git clone https://github.com/jorige3/freelance-project-finder-agent.git
cd freelance-project-finder-agent

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

### Development Dependencies

```bash
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

### Start the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```

The API will be available at http://localhost:8010.

### Seed Database with Sample Data

```bash
curl -X POST http://localhost:8010/projects/seed
```

### Collect Live Opportunities

```bash
curl -X POST http://localhost:8010/collect
```

### Get Top Free Gigs

```bash
curl "http://localhost:8010/agents/top-free-gigs?limit=5"
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 📡 API Endpoints

### Health & Status

```http
GET /
GET /health
```

### Project Management

```http
POST /projects/seed
GET /projects
POST /collect
```

### Score & Proposal

```http
GET /projects/{project_id}/score
GET /projects/{project_id}/proposal
```

### Application Tracking

```http
GET /projects/{project_id}/application
PATCH /projects/{project_id}/application
```

### Agent Endpoints

```http
GET /agents/top-free-gigs?limit=5
```

The application supports the following application statuses: saved, proposal_ready, applied, interview, offer, completed, and rejected.

---

## 📁 Project Structure

```
freelance-project-finder-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application & endpoints
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── collector_agent.py     # Orchestrates project collection
│   │   ├── filter_agent.py        # Filters for free-to-apply & tech jobs
│   │   ├── ranking_agent.py       # Explains project scores
│   │   ├── proposal_agent.py      # Generates proposals
│   │   └── coordinator.py         # Main orchestrator agent
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py                # Base collector interface
│   │   ├── manager.py             # Manages multiple collectors
│   │   ├── remoteok.py            # RemoteOK.com scraper
│   │   └── mock_collector.py      # Sample data provider
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py              # SQLAlchemy ORM models
│   │   └── session.py             # Database session setup
│   ├── ranking/
│   │   ├── __init__.py
│   │   └── scorer.py              # Scoring engine with skill weights
│   ├── proposal/
│   │   ├── __init__.py
│   │   └── generator.py           # Proposal generation logic
│   └── services/
│       └── [future service modules]
├── dashboard/
│   └── app.py                     # Streamlit dashboard UI
├── data/
│   └── [database files]
├── scripts/
│   └── [utility scripts]
├── tests/
│   └── [test files]
├── pyproject.toml                 # Project metadata & dependencies
├── README.md                      # This file
└── main.py                        # Entry point
```

---

## ⚙️ Configuration

### Environment Variables

The application can be configured by defining environment variables. You can optionally place them in a `.env` file in the project root:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | Base URL of the FastAPI backend API | `http://localhost:8010` |
| `DATABASE_URL` | SQLAlchemy SQLite database connection string | `sqlite:///./freelance_projects.db` |
| `OLLAMA_BASE_URL` | Base endpoint URL of the local Ollama server | `http://localhost:11434` |
| `OLLAMA_PROPOSAL_MODEL` | Ollama model utilized for AI proposals | `qwen3:1.7b` |
| `OLLAMA_TIMEOUT` | Timeout limit (in seconds) for proposal generation | `120` |

---

### Skill Weights (Scoring)

Edit `app/ranking/scorer.py` to adjust scoring:

```python
SKILL_WEIGHTS = {
    "python": 25,        # Highest weight for core skill
    "fastapi": 25,
    "api": 15,
    "automation": 20,
    "ai": 20,
    "machine learning": 20,
    "docker": 15,
    "devops": 15,
    # ... more skills
}
```

### Filtering Thresholds

Edit `app/agents/filter_agent.py`:

```python
MIN_SCORE_THRESHOLD = 50  # Minimum score to recommend
```

### Difficulty Keywords

Edit `app/ranking/scorer.py`:

```python
EASY_KEYWORDS = {
    "simple", "small", "easy", "junior", "entry level", "script", "automation"
}

NEGATIVE_KEYWORDS = {
    "senior": -10,
    "lead": -15,
    "manager": -20,
    "director": -25,
}
```

---

## 💡 Usage Examples

### Example 1: Get Top 3 Free Gigs

```bash
curl "http://localhost:8010/agents/top-free-gigs?limit=3" | jq
```

**Response:**
```json
{
  "agent": "CoordinatorAgent",
  "total": 3,
  "projects": [
    {
      "id": 1,
      "title": "Build FastAPI CRUD backend",
      "platform": "Mock",
      "score": 100,
      "budget": "$250",
      "skills": "Python, FastAPI, SQLite",
      "url": "https://example.com/project1",
      "explanation": {
        "score": 100,
        "reasons": [
          "Base score +30",
          "Matched skill 'python' +25",
          "Matched skill 'fastapi' +25",
          "Matched skill 'backend' +15",
          "Beginner-friendly keyword 'simple' +5",
          "Score capped from 110 to 100"
        ]
      },
      "proposal": "Hello,\n\nI can help you with \"Build FastAPI CRUD backend\"...\n"
    }
  ]
}
```

### Example 2: Explain Score for Project

```bash
curl "http://localhost:8010/projects/1/score"
```

### Example 3: Generate Proposal

```bash
curl "http://localhost:8010/projects/1/proposal"
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Additional job board integrations (Upwork, Freelancer, Toptal)
- [ ] Machine learning-based scoring refinement
- [ ] User authentication and personalized recommendations
- [ ] Email notifications for matching opportunities
- [ ] Advanced filtering by location, timezone, payment method
- [ ] Portfolio integration suggestions
- [ ] Test coverage improvements

**Process:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 👨‍💻 Author

**Kishore Kumar Jorige**  
- GitHub: [@jorige3](https://github.com/jorige3)

Special thanks to **OpenAI's ChatGPT** for assistance throughout design, implementation, debugging, and documentation.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🌟 Vision & Roadmap

**Vision:** Build an open, practical platform that helps developers and freelancers discover quality opportunities more efficiently through intelligent filtering and personalized recommendations.

**Future Roadmap:**
- v1.1: Email digest delivery system
- v1.2: User authentication and saved preferences
- v1.3: ML-based opportunity recommendation refinement
- v2.0: Multi-board aggregation with unified interface
- v2.1: Portfolio-aware recommendations

---

## ⭐ If you find this useful, please star the repository!