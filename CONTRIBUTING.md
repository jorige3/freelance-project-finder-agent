# Contributing to Freelance Project Finder AI Agent

Thank you for considering contributing to this project! Contributions are what make this project better for everyone.

## Code of Conduct

Please be respectful and constructive in all interactions. We're building a welcoming community.

---

## How Can I Contribute?

### 1. **Report Bugs**
If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and dependencies installed
- Any error logs or stack traces

### 2. **Suggest Enhancements**
Have an idea for improvement? Create an issue describing:
- What problem it solves
- How it would improve the project
- Possible implementation approach

### 3. **Submit Pull Requests**
Code contributions are welcome!

#### Pull Request Process:
1. **Fork the repository** and create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guide below

3. **Write/update tests** if applicable

4. **Update documentation** if adding new features

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: feature description"
   git commit -m "Fix: bug description"
   git commit -m "Docs: documentation update"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshot/demo if UI changes
   - Test results

---

## Development Setup

### Prerequisites
- Python 3.11+
- Git
- Virtual environment tool (venv or conda)

### Local Setup

```bash
# Clone your fork
git clone https://github.com/your-username/freelance-project-finder-agent.git
cd freelance-project-finder-agent

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Running the Project

```bash
# Start the API server
uvicorn app.main:app --reload --port 8010

# In another terminal, start the dashboard
streamlit run dashboard/app.py

# Run tests
pytest tests/

# Run linting
ruff check app/
```

---

## Code Style Guide

### Python Standards
- **Style**: Follow [PEP 8](https://pep8.org/)
- **Formatter**: Use `black` for code formatting
- **Linter**: Use `ruff` for linting
- **Type Hints**: Include type hints where practical

### Naming Conventions
- Classes: `CamelCase` (e.g., `FilterAgent`)
- Functions/methods: `snake_case` (e.g., `filter_projects()`)
- Constants: `UPPER_CASE` (e.g., `MIN_SCORE_THRESHOLD`)
- Private methods: prefix with `_` (e.g., `_helper_method()`)

### Code Organization
```python
# 1. Standard library imports
import re
from pathlib import Path

# 2. Third-party imports
from sqlalchemy import Column, String
from pydantic import BaseModel

# 3. Local imports
from app.database.models import FreelanceProject

# 4. Constants
MIN_SCORE = 50

# 5. Classes and functions
class MyClass:
    pass

def my_function():
    pass
```

### Docstring Format
Use Google-style docstrings:

```python
def calculate_score(project: CollectedProject) -> int:
    """Calculate and return the score for a project.
    
    Evaluates the project based on skill matches, difficulty level,
    and negative keywords like senior/director positions.
    
    Args:
        project: The project to score
        
    Returns:
        An integer score between 0-100
        
    Raises:
        ValueError: If project data is invalid
    """
    pass
```

---

## Key Areas for Contribution

### High Priority
- [ ] Additional job board integrations (Upwork, Freelancer, Toptal)
- [ ] User authentication system
- [ ] Email digest notifications
- [ ] Advanced filtering UI improvements
- [ ] Test coverage (currently low)

### Medium Priority
- [ ] Performance optimization for large datasets
- [ ] Caching strategy implementation
- [ ] Logging improvements
- [ ] API documentation in OpenAPI/Swagger format
- [ ] Database migration system

### Nice to Have
- [ ] Portfolio analysis integration
- [ ] Interview prep recommendations
- [ ] Salary insights and benchmarks
- [ ] Community project showcase
- [ ] Docker containerization

---

## Testing

### Writing Tests

```python
# tests/test_scorer.py
import pytest
from app.ranking.scorer import score_project, explain_score_project
from app.collectors.base import CollectedProject

def test_score_python_project():
    """Test that Python projects score correctly."""
    project = CollectedProject(
        title="Python Script",
        description="Write a Python script",
        skills="Python, Automation",
        budget="$100",
        difficulty="easy"
    )
    score = score_project(project)
    assert score > 50  # Should score well

def test_negative_keyword_penalty():
    """Test that senior positions are penalized."""
    project = CollectedProject(
        title="Senior Developer",
        skills="Python",
        budget="$5000"
    )
    score = score_project(project)
    assert score < 50  # Should be penalized
```

### Running Tests
```bash
pytest tests/                    # Run all tests
pytest tests/test_scorer.py      # Run specific file
pytest -v                        # Verbose output
pytest --cov=app                 # Coverage report
```

---

## Documentation

### Updating Documentation
- **README.md**: Overview, setup, quick start
- **API.md**: API endpoints, parameters, responses
- **CONTRIBUTING.md**: This file
- **Code Comments**: Inline explanations for complex logic
- **Docstrings**: Function and class documentation

### Documentation Standards
- Use clear, simple language
- Include examples where helpful
- Keep links up-to-date
- Use proper Markdown formatting
- Add table of contents for long documents

---

## Commit Message Guidelines

Use clear, descriptive commit messages following this format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Build, dependencies, CI/CD

### Scope
The area affected: `scorer`, `agents`, `api`, `database`, etc.

### Examples
```
feat(scorer): add word boundary matching for keywords

This fixes false positives like "ai" matching "admin".
Uses regex word boundaries for all keyword matching.

Fixes #42
```

```
fix(filter_agent): correct tech job detection

Non-tech roles were incorrectly identified as tech jobs.
Updated keyword list and matching logic.
```

---

## Review Process

1. **Automated Checks**: Tests, linting, and type checking must pass
2. **Code Review**: At least one maintainer review
3. **Documentation**: Must include relevant documentation updates
4. **Testing**: New features should include tests

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] No new linting errors
- [ ] Documentation updated
- [ ] Commits are well-organized
- [ ] No secrets/credentials in code

---

## Questions?

- **Documentation**: Check [README.md](README.md) and [API.md](API.md)
- **Issues**: Search existing issues first
- **Discussions**: Create a discussion for questions
- **Contact**: Reach out to the maintainer

---

## Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Project release notes
- GitHub contributors page

Thank you for contributing! 🎉
