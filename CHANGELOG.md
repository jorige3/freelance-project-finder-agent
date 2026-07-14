# Changelog

All notable changes to the Freelance Project Finder AI Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [0.8.0] - 2026-07-13

### Added
- MIT license.
- Environment-variable documentation.
- Root CLI launcher for the API and Streamlit dashboard.

### Changed
- Centralized ORM-to-DTO conversion with `CollectedProject.from_orm()`.
- Improved README, API, and architecture documentation.
- Restored the verified GitHub Actions workflow using `checkout@v5` and `setup-uv@v6`.

### Fixed
- Broken API documentation formatting.
- Inconsistent project version metadata.


### Initial Release

This is the first major release of the Freelance Project Finder AI Agent.

#### Added
- **Core Scoring Engine**
  - Base score system (30 points + modifiers)
  - 16 skill weights (Python, FastAPI, API, Automation, ML, etc.)
  - Beginner-friendly keyword bonuses
  - Negative keyword penalties (senior, lead, manager, director)
  - Score capping at 0-100 range
  - Explainable scoring with detailed reasons

- **Agent System**
  - CoordinatorAgent: Main orchestrator for workflows
  - CollectorAgent: Manages project collection from multiple sources
  - FilterAgent: Applies business logic filters
  - RankingAgent: Explains project scores
  - ProposalAgent: Generates contextual proposals
  - Well-defined agent interfaces for extensibility

- **Job Type Detection**
  - Intelligent tech job detection using 25+ keywords
  - Word boundary matching to avoid false positives
  - Distinction between tech and non-tech roles
  - Proper handling of "AI" substring matching in admin roles

- **Proposal Generation**
  - Tech-focused proposals for development roles
  - Polite decline templates for non-tech opportunities
  - Context-aware templates based on job type
  - Personalized content using project skills

- **Intelligent Filtering**
  - Free-to-apply opportunity filter
  - Tech relevance filter (development jobs only)
  - Minimum score threshold (50+)
  - Chainable filter methods in FilterAgent

- **Data Collection**
  - RemoteOK.com web scraper using BeautifulSoup
  - Mock collector for testing/development
  - CollectorManager for multi-source coordination
  - Automatic deduplication on collection
  - Collection statistics and reporting

- **REST API**
  - FastAPI backend with full routing
  - Project CRUD operations
  - Score explanation endpoints
  - Proposal generation endpoints
  - Main `/agents/top-free-gigs` workflow endpoint
  - Health checks and status endpoints

- **Database**
  - SQLite persistence with SQLAlchemy ORM
  - FreelanceProject model with 10+ fields
  - Proper indexing for performance
  - Session management with dependency injection

- **Documentation**
  - Comprehensive README.md
  - API endpoint documentation
  - Architecture and design documentation
  - Contributing guidelines
  - Changelog (this file)

### Features
- ✅ Collect live freelance opportunities
- ✅ AI-powered intelligent ranking
- ✅ Explainable scoring with detailed reasoning
- ✅ Smart filtering for free-to-apply tech jobs
- ✅ Contextual proposal generation
- ✅ RESTful FastAPI backend
- ✅ SQLite database persistence
- ✅ Multi-source data collection
- ✅ Deduplication system
- ✅ Modular agent architecture

### Technical Details
- Python 3.11+
- FastAPI 0.139+
- SQLAlchemy 2.0+
- BeautifulSoup4 4.15+
- Uvicorn 0.50+

### Known Limitations
- Single platform focus (RemoteOK + Mock)
- No user authentication
- No email notifications
- Limited to developer roles
- No caching system yet
- Synchronous collectors (can be slow)

---

## [0.1.0] - 2026-06-15

### Alpha Release (Pre-release)

Initial development version with basic functionality.

#### Added
- Basic project model and database schema
- Simple scoring algorithm
- FastAPI application skeleton
- Mock data collector
- Initial API endpoints

#### Known Issues
- Inconsistent keyword matching causing false positives
- Generic proposals for all job types
- No tech job filtering
- High false positive rate in scoring

---

## Unreleased (Development)

### Planned for v0.9.0
- [ ] Asynchronous opportunity collection
  - Refactor scrapers to use `httpx.AsyncClient`
  - Introduce timeout limits on feeds and HTTP parser connections
  - Deduplication batch optimization (eliminate N+1 queries)
- [ ] Database session safety & SQLite WAL mode
  - Defer session holds during external calls (Ollama API)
  - Configure connection pool & WAL mode
  - Unique constraint/index on `url`
- [ ] Test coverage expansion
  - API endpoint integration tests
  - Mock collector tests and LLM fallback tests

### Planned for v1.0.0
- [ ] User authentication and API access controls
- [ ] Email digest notification delivery
- [ ] Advanced UI filter configurations

---

## [0.2.0] to [0.7.0] - Various Dates (2026)

- Development iterations addressing keyword scoring boundary matching, tech/non-tech detection classifiers, Streamlit dashboard interface updates, and core agent orchestration pipelines.

---

## Migration Guides

### From Pre-release to v0.8.0

**Breaking Changes**: None - this is the first major release.

**Database Migration**: 
- No migration needed (new database schema).
- If upgrading from alpha, back up your `data/` directory.

**API Changes**:
- Endpoints remain stable.
- Scoring logic and tech filtering updates might reduce low-relevance recommendations compared to the alpha version.

---

## Performance Notes (v0.8.0)

> [!NOTE]
> Performance metrics are estimates based on a typical local development environment (WSL2/Ubuntu).

- Startup time: ~1-2 seconds
- Estimated API response time: 
  - `/health`: <10ms
  - `/agents/top-free-gigs`: 50-200ms (dependent on local database size)
  - `/collect`: 5-30 seconds (dependent on network speeds and external rate limiting)
- Database size: ~1MB per 1000 projects
- Memory footprint: ~100MB typical

---

## Deprecation Notices

None.

---

## Contributors

- **Kishore Kumar Jorige** - Creator and maintainer
- **OpenAI ChatGPT** - Development assistance

---

## For More Information

- [README.md](README.md) - Project overview
- [API.md](API.md) - API documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

## Release Checklist

For maintainers creating new releases:

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `app/main.py`
- [ ] Add section to CHANGELOG.md
- [ ] Create GitHub Release with tag
- [ ] Update README.md if needed
- [ ] Announce in project issues/discussions
- [ ] Update documentation website if applicable

---

## Support

For issues or questions about changes:
1. Check the Changelog for relevant version
2. See [API.md](API.md) for endpoint changes
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) for design changes
4. Open an issue on GitHub

---

**Last Updated**: 2026-07-09  
**Maintained By**: Kishore Kumar Jorige
