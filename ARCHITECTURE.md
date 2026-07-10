# Architecture & Design Document

## System Overview

The Freelance Project Finder AI Agent is built on a modular, agent-based architecture that emphasizes separation of concerns and extensibility.

```
┌─────────────────────────────────────────────────────┐
│                  API Layer (FastAPI)                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Endpoints:                                         │
│  ├─ /projects/* (CRUD operations)                  │
│  ├─ /projects/{id}/score (explain scoring)         │
│  ├─ /projects/{id}/proposal (generate proposal)    │
│  └─ /agents/top-free-gigs (coordinated workflow)   │
│                                                     │
├─────────────────────────────────────────────────────┤
│                 Orchestration Layer                 │
│                                                     │
│  ┌─────────────┐                                   │
│  │ Coordinator │  (Main orchestrator agent)        │
│  │   Agent     │                                   │
│  └─────────────┘                                   │
│         ↓                                           │
├─────────────────────────────────────────────────────┤
│               Processing Agents                     │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │  Collector   │  │   Filter     │               │
│  │   Agent      │  │   Agent      │               │
│  └──────────────┘  └──────────────┘               │
│         ↓                  ↓                       │
│  ┌──────────────┐  ┌──────────────┐               │
│  │   Ranking    │  │   Proposal   │               │
│  │   Agent      │  │   Agent      │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
├─────────────────────────────────────────────────────┤
│              Business Logic Layer                   │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │  Scorers &   │  │   Collectors │               │
│  │  Analyzers   │  │   Managers   │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
├─────────────────────────────────────────────────────┤
│               Data Layer (Database)                 │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │      SQLite Database                          │ │
│  │  ├─ freelance_projects (main table)           │ │
│  │  └─ (other future tables)                     │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
├─────────────────────────────────────────────────────┤
│              External Data Sources                  │
│                                                     │
│  ├─ RemoteOK API                                  │
│  ├─ Mock Collector (sample data)                  │
│  └─ (Future: Upwork, Freelancer, etc.)           │
└─────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. API Layer (`app/main.py`)

**Purpose**: HTTP interface for accessing project data and agent workflows

**Responsibilities**:
- Route HTTP requests to appropriate handlers
- Manage database sessions
- Return JSON responses
- Handle error cases

**Key Functions**:
```python
@app.get("/agents/top-free-gigs")
def top_free_gigs(limit: int = 5, db: Session = Depends(get_db)):
    """Main endpoint orchestrating the entire workflow"""
```

### 2. Agent System (`app/agents/`)

Agents are autonomous components that perform specific tasks in the workflow.

#### **CoordinatorAgent** (`coordinator.py`)
- **Role**: Orchestrates all other agents
- **Workflow**:
  1. Collects projects
  2. Filters for free-to-apply jobs
  3. Filters for relevant tech jobs
  4. Ranks projects by score
  5. Generates proposals
  6. Returns compiled results

```python
def get_top_free_gigs(self, db: Session, limit: int = 5):
    # Step 1: Get all projects sorted by score
    projects = db.query(FreelanceProject).order_by(...).all()
    
    # Step 2: Apply free-to-apply filter
    free_projects = self.filter_agent.free_to_apply(projects)
    
    # Step 3: Apply tech relevance filter
    relevant_projects = self.filter_agent.relevant_jobs(free_projects)
    
    # Step 4-5: Score and generate proposals
    return [self._format_project(p) for p in relevant_projects[:limit]]
```

#### **CollectorAgent** (`collector_agent.py`)
- **Role**: Orchestrates data collection from multiple sources
- **Responsibilities**:
  - Manages multiple collectors
  - Handles deduplication
  - Updates database
  - Returns collection stats

#### **FilterAgent** (`filter_agent.py`)
- **Role**: Applies business logic filters
- **Filters**:
  - `free_to_apply()`: Only free application opportunities
  - `relevant_jobs()`: Only tech/development jobs (MIN_SCORE_THRESHOLD: 50+)

#### **RankingAgent** (`ranking_agent.py`)
- **Role**: Explains project scores
- **Functionality**:
  - Returns stored score
  - Provides scoring breakdown
  - Shows reasoning with list of factors

#### **ProposalAgent** (`proposal_agent.py`)
- **Role**: Generates contextual proposals
- **Functionality**:
  - Calls proposal generator
  - Returns formatted proposal
  - Can detect non-tech jobs and provide appropriate response

---

### 3. Scoring System (`app/ranking/scorer.py`)

**Purpose**: Calculate project relevance scores with explainable reasoning

**Scoring Algorithm**:

```
Base Score: 30 points

+ Skill Matches (weighted by skill_weights dictionary)
  - Python: +25
  - FastAPI: +25
  - API: +15
  - Automation: +20
  - Machine Learning: +20
  - etc...

+ Beginner Keywords (+5 each)
  - "simple", "small", "easy", "junior", "entry level", "script", "automation"

+ Negative Keywords (penalties)
  - "senior": -10
  - "lead": -15
  - "manager": -20
  - "director": -25
  - "casino"/"gambling": -30

Final Score: min(max(calculated_score, 0), 100)  # Cap 0-100
```

**Key Features**:
- Word boundary matching to avoid false positives ("ai" vs "admin")
- Explainable reasoning - shows all factors affecting score
- Capped at 0-100 range

```python
def explain_score_project(project: CollectedProject) -> ScoreResult:
    """
    Returns:
        ScoreResult with:
        - score (int): Final score 0-100
        - reasons (list[str]): Explanation of scoring
    """
```

---

### 4. Job Type Detection (`app/proposal/generator.py`)

**Purpose**: Distinguish tech jobs from non-tech jobs

**Detection Logic**:
```python
def is_tech_job(project: FreelanceProject) -> bool:
    """
    Searches project title, description, and skills for tech keywords
    using word boundaries to avoid false matches.
    
    Tech Keywords:
    - Languages: python, java, javascript, typescript
    - Frameworks: fastapi, django, flask, react, vue
    - Concepts: api, database, backend, devops, automation
    - Roles: developer, engineer, programmer
    """
```

**Why This Matters**:
- Non-tech jobs (admin, support, marketing) shouldn't get dev proposals
- Filters prevent recommending irrelevant opportunities
- Personalized proposals based on actual job type

---

### 5. Proposal Generation (`app/proposal/generator.py`)

**Purpose**: Generate contextual, personalized proposals

**Logic**:
```
IF is_tech_job(project):
    └─ Generate technical proposal focused on:
       - Skill demonstration
       - Development approach
       - Quality commitment
ELSE:
    └─ Generate polite decline:
       - Thank for opportunity
       - Explain expertise mismatch
       - Recommend specialist
```

---

### 6. Collectors System (`app/collectors/`)

**Purpose**: Fetch projects from external sources

#### **Base Collector** (`base.py`)
```python
class BaseCollector:
    def collect(self) -> list[CollectedProject]:
        """Must be implemented by subclasses"""
        pass
```

#### **RemoteOK Collector** (`remoteok.py`)
- Scrapes RemoteOK.com using BeautifulSoup
- Parses HTML to extract job details
- Filters for Python/FastAPI opportunities

#### **Mock Collector** (`mock_collector.py`)
- Provides sample data for testing
- Useful for development without external API calls

#### **Collector Manager** (`manager.py`)
- Orchestrates multiple collectors
- Handles deduplication (checks if project already exists)
- Returns aggregated results

```python
class CollectorManager:
    def collect_all(self, db: Session) -> dict:
        """
        Collects from all configured collectors,
        deduplicates, and stores in database
        
        Returns: {
            "status": "success",
            "total_found": int,
            "inserted": int,
            "duplicates_skipped": int
        }
        """
```

---

### 7. Database Layer (`app/database/`)

#### **Models** (`models.py`)
```python
class FreelanceProject(Base):
    """ORM model for projects table"""
    
    id: int (Primary Key)
    title: str
    platform: str
    url: str
    description: str
    budget: str
    skills: str
    difficulty: str
    score: int
    status: str
    created_at: datetime
    is_free_to_apply: str
    apply_cost: str
    opportunity_type: str
```

#### **Session Management** (`session.py`)
- SQLAlchemy session configuration
- Database connection setup
- Session factory for dependency injection

---

## Data Flow Examples

### Example 1: Get Top Free Gigs

```
User Request: GET /agents/top-free-gigs?limit=5
    ↓
FastAPI Router
    ↓
CoordinatorAgent.get_top_free_gigs()
    ↓
1. Query all projects sorted by score DESC
    ↓
2. FilterAgent.free_to_apply() → Filter where is_free_to_apply == "yes"
    ↓
3. FilterAgent.relevant_jobs() → Filter tech jobs with score >= 50
    ↓
4. Take first 5 projects
    ↓
5. For each project:
    - RankingAgent.explain() → Get score explanation
    - ProposalAgent.generate() → Generate proposal
    ↓
6. Return formatted JSON response
    ↓
Response: { projects: [...], total: 5, agent: "CoordinatorAgent" }
```

### Example 2: Score Explanation

```
User Request: GET /projects/1/score
    ↓
FastAPI Router
    ↓
1. Fetch project from database
    ↓
2. Convert to CollectedProject (DTO)
    ↓
3. explain_score_project(project)
    ↓
4. Calculate:
    - Base score: 30
    - Skill matches (keyword_found with regex)
    - Bonus keywords
    - Negative keywords
    ↓
5. Cap score 0-100
    ↓
6. Return { score, reasons: [...] }
    ↓
Response: { id, title, score, reasons: [...] }
```

### Example 3: Collect & Filter Projects

```
User Request: POST /collect
    ↓
CollectorAgent.run()
    ↓
CollectorManager.collect_all()
    ↓
1. RemoteOKCollector.collect() → Scrape RemoteOK
2. MockCollector.collect() → Load sample data
    ↓
3. For each collected project:
    - Check if already in database (dedup)
    - Calculate score with scorer.score_project()
    - Insert or skip
    ↓
4. Return { total_found, inserted, duplicates_skipped }
    ↓
Response: { status: "success", ... }
```

---

## Design Patterns Used

### 1. **Agent Pattern**
Each agent encapsulates a specific responsibility:
- Clear interface (usually one main method)
- Can be called independently or as part of workflow
- Promotes testability and modularity

### 2. **Strategy Pattern**
Collectors implement a common interface:
- Can swap collectors without changing main logic
- Easy to add new sources
- Decouples collection logic from orchestration

### 3. **Dependency Injection**
FastAPI's `Depends()` manages:
- Database session lifecycle
- Transaction management
- Resource cleanup

### 4. **Data Transfer Objects (DTO)**
`CollectedProject` separate from `FreelanceProject`:
- Decouples external schema from internal model
- Allows flexibility in data transformation
- Cleaner API boundaries

### 5. **Repository Pattern** (Implicit)
Database access is centralized in models:
- Single source of truth for queries
- Easy to modify database logic
- Testable with mocks

---

## Extension Points

### Adding a New Collector

```python
# 1. Create new collector
class MyCollector(BaseCollector):
    def collect(self) -> list[CollectedProject]:
        # Your scraping/API logic here
        pass

# 2. Register in CollectorManager
class CollectorManager:
    def __init__(self):
        self.collectors = [
            RemoteOKCollector(),
            MockCollector(),
            MyCollector(),  # Add here
        ]
```

### Modifying Scoring

```python
# Edit app/ranking/scorer.py
SKILL_WEIGHTS = {
    "python": 25,
    "rust": 30,  # Add new skill
    # ...
}

NEGATIVE_KEYWORDS = {
    "remote": -5,  # Add new penalty
    # ...
}
```

### Adding New Filters

```python
# In filter_agent.py
def high_paying(self, projects) -> list[FreelanceProject]:
    return [p for p in projects if self._extract_budget(p) > 500]

# In coordinator.py
relevant_projects = self.filter_agent.relevant_jobs(free_projects)
high_paying_projects = self.filter_agent.high_paying(relevant_projects)
```

### New API Endpoint

```python
# In app/main.py
@app.get("/agents/top-remote-jobs")
def top_remote_jobs(db: Session = Depends(get_db)):
    # Coordinator variant for remote-specific logic
    pass
```

---

## Performance Considerations

### Current Optimizations
1. **Database Indexing**: Score column indexed for fast sorting
2. **Query Filtering**: Large filters applied at database level
3. **Lazy Loading**: Only load projects when needed

### Future Improvements
1. **Caching**: Cache top-gigs results for 1 hour
2. **Pagination**: Support large datasets with offset/limit
3. **Async Collectors**: Run collectors concurrently
4. **Database Connection Pooling**: Reuse connections
5. **Search Indexing**: Full-text search on title/skills

---

## Testing Strategy

### Unit Tests
- Test individual scorer functions
- Test filter logic in isolation
- Test keyword matching

### Integration Tests
- Test agent workflows end-to-end
- Test API endpoints with real database
- Test collector implementations

### Mock Setup
```python
# Use mock_collector for testing without external APIs
manager = CollectorManager()
collector = MockCollector()
projects = collector.collect()
```

---

## Error Handling

### Current Approach
- Try-catch blocks around external API calls
- Database session cleanup with finally blocks
- HTTP exception responses

### Future Improvements
- Structured error logging
- Retry logic for transient failures
- Circuit breaker for failing APIs
- Graceful degradation

---

## Glossary

- **Agent**: Autonomous component responsible for one task
- **Collector**: Component that fetches projects from external source
- **Scoring**: Calculation of project relevance to developer
- **Filter**: Logic that removes ineligible projects
- **Proposal**: Generated cover letter for applying to project
- **DTO**: Data Transfer Object (data container for APIs)
- **ORM**: Object-Relational Mapping (SQLAlchemy)

---

## See Also

- [README.md](README.md) - Project overview
- [API.md](API.md) - API endpoint documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
