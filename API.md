# API Documentation

## Base URL
```
http://localhost:8010
```

## Overview

This document describes all available endpoints for the Freelance Project Finder API.

---

## Endpoints

### Health & Status

#### GET `/`
Health check and basic info endpoint.

**Response:**
```json
{
  "status": "running",
  "project": "Freelance Project Finder AI Agent",
  "version": "0.2.0"
}
```

---

#### GET `/health`
Simple health check.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Projects

#### POST `/projects/seed`
Seed the database with sample projects for testing and demonstration.

**Parameters:** None

**Response:**
```json
{
  "message": "Seeded X projects",
  "projects_added": 5
}
```

---

#### GET `/projects`
Retrieve all projects from the database.

**Query Parameters:**
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100) - Number of records to return

**Response:**
```json
[
  {
    "id": 1,
    "title": "Build FastAPI CRUD backend",
    "platform": "Mock",
    "url": "https://example.com/project",
    "description": "Need a simple FastAPI backend with SQLite database.",
    "budget": "$250",
    "skills": "Python, FastAPI, SQLite",
    "difficulty": "easy",
    "score": 100,
    "status": "new",
    "created_at": "2026-07-09T00:00:00",
    "is_free_to_apply": "yes",
    "apply_cost": "free",
    "opportunity_type": "remote_job"
  }
]
```

---

#### POST `/collect`
Collect fresh opportunities from configured collectors (RemoteOK, mock data, etc.).

**Parameters:** None

**Response:**
```json
{
  "status": "success",
  "total_found": 27,
  "inserted": 5,
  "duplicates_skipped": 22
}
```

---

### Scoring & Analysis

#### GET `/projects/{project_id}/score`
Get the detailed scoring explanation for a specific project.

**Path Parameters:**
- `project_id` (int, required) - The ID of the project

**Response:**
```json
{
  "id": 1,
  "title": "Build FastAPI CRUD backend",
  "platform": "Mock",
  "stored_score": 100,
  "calculated_score": 100,
  "reasons": [
    "Base score +30",
    "Matched skill 'python' +25",
    "Matched skill 'fastapi' +25",
    "Matched skill 'sqlite' +10",
    "Matched skill 'backend' +15",
    "Beginner-friendly keyword 'simple' +5",
    "Score capped from 110 to 100"
  ]
}
```

---

#### GET `/projects/{project_id}/proposal`
Generate a tailored proposal/cover letter for a specific project.

**Path Parameters:**
- `project_id` (int, required) - The ID of the project

**Response:**
```json
{
  "id": 1,
  "title": "Build FastAPI CRUD backend",
  "platform": "Mock",
  "proposal": "Hello,\n\nI can help you with \"Build FastAPI CRUD backend\".\n\nI have hands-on experience with Python, FastAPI, SQLite. I can understand your requirement, build a clean working solution, and provide simple setup instructions so you can run it easily.\n\nMy approach:\n1. Review the requirement clearly.\n2. Build a small working version first.\n3. Test it properly.\n4. Improve it based on your feedback.\n5. Deliver clean code with basic documentation.\n\nI focus on practical, reliable, and easy-to-maintain solutions.\n\nThank you,\nKishore Kumar Jorige\n"
}
```

---

### Agent Endpoints

#### GET `/agents/top-free-gigs`
Get the top recommended free-to-apply tech opportunities based on intelligent filtering and scoring.

**Query Parameters:**
- `limit` (int, default: 5) - Number of opportunities to return

**Filters Applied:**
1. Only free-to-apply opportunities
2. Only tech/development-related jobs (using keyword matching)
3. Minimum score threshold (50+)
4. Sorted by score descending

**Response:**
```json
{
  "agent": "CoordinatorAgent",
  "total": 5,
  "projects": [
    {
      "id": 1,
      "title": "Build FastAPI CRUD backend",
      "platform": "Mock",
      "score": 100,
      "budget": "$250",
      "skills": "Python, FastAPI, SQLite",
      "url": "https://example.com/project",
      "explanation": {
        "score": 100,
        "reasons": [
          "Base score +30",
          "Matched skill 'python' +25",
          "Matched skill 'fastapi' +25",
          "Matched skill 'sqlite' +10",
          "Matched skill 'backend' +15",
          "Beginner-friendly keyword 'simple' +5",
          "Score capped from 110 to 100"
        ]
      },
      "proposal": "Hello,\n\nI can help you with \"Build FastAPI CRUD backend\"...\n"
    },
    {
      "id": 2,
      "title": "Python script for file automation",
      "platform": "Mock",
      "score": 85,
      "budget": "$100",
      "skills": "Python, Automation, Files",
      "url": "https://example.com/automation",
      "explanation": {
        "score": 85,
        "reasons": [
          "Base score +30",
          "Matched skill 'python' +25",
          "Matched skill 'automation' +20",
          "Beginner-friendly keyword 'script' +5",
          "Beginner-friendly keyword 'automation' +5"
        ]
      },
      "proposal": "Hello,\n\nI can help you with \"Python script for file automation\"...\n"
    }
  ]
}
```

---

## Error Responses

### 404 - Not Found
When a resource is not found:

```json
{
  "error": "Project not found"
}
```

---

### 500 - Internal Server Error
When an unexpected error occurs:

```json
{
  "detail": "Internal server error message"
}
```

---

## Scoring System

### Base Score
- Every project starts with **30 points**

### Skill Weights
Matched skills from the project add points:

| Skill | Points |
|-------|--------|
| Python | 25 |
| FastAPI | 25 |
| API | 15 |
| Automation | 20 |
| AI / Machine Learning | 20 |
| Data Science | 15 |
| Docker | 15 |
| DevOps | 15 |
| Linux | 10 |
| SQLite | 10 |
| Backend | 15 |
| Cloud / Azure / AWS | 10 |

### Ease Keywords
Projects marked as "easy" get bonus points:

| Keyword | Bonus |
|---------|-------|
| simple, small, easy, junior, entry level, beginner, script, automation | +5 |

### Negative Keywords
Projects with negative keywords are penalized:

| Keyword | Penalty |
|---------|---------|
| Senior | -10 |
| Lead | -15 |
| Manager | -20 |
| Director | -25 |
| Casino / Gambling | -30 |

### Score Capping
Final score is capped between 0-100.

---

## Filtering Logic

### Tech Job Detection
A project is considered a **tech/development job** if it contains any of these keywords (using word boundaries):

```
python, java, javascript, typescript, react, vue, angular, fastapi, 
django, flask, nodejs, backend, frontend, fullstack, api, database, 
sql, mongodb, docker, kubernetes, devops, machine learning, 
artificial intelligence, data science, automation, script, coding, 
development, engineer, developer, programmer, software, web dev, 
web development
```

### Free-to-Apply Filter
Only projects with `is_free_to_apply == "yes"` are included.

### Minimum Score Threshold
Only projects with `score >= 50` are recommended.

---

## Rate Limiting
Currently no rate limiting is implemented. In production, consider adding:
- Rate limiting per IP
- Authentication tokens with quotas
- Caching for frequently accessed endpoints

---

## Best Practices

1. **Pagination**: Use `skip` and `limit` for large datasets
2. **Caching**: Cache `/agents/top-free-gigs` results for 1 hour
3. **Error Handling**: Always check response status codes
4. **Proposal Generation**: Only generate proposals for tech jobs to avoid irrelevant content
5. **Score Explanation**: Always show users the reasoning behind scores

---

## Example Usage

### Python with Requests

```python
import requests

base_url = "http://localhost:8010"

# Get top 3 free gigs
response = requests.get(f"{base_url}/agents/top-free-gigs?limit=3")
projects = response.json()["projects"]

for project in projects:
    print(f"Title: {project['title']}")
    print(f"Score: {project['score']}")
    print(f"Proposal:\n{project['proposal']}")
    print("---")
```

### cURL

```bash
# Get top free gigs
curl "http://localhost:8010/agents/top-free-gigs?limit=5" | jq

# Get score explanation
curl "http://localhost:8010/projects/1/score" | jq

# Generate proposal
curl "http://localhost:8010/projects/1/proposal" | jq
```

### JavaScript/Fetch

```javascript
async function getTopGigs(limit = 5) {
  const response = await fetch(`http://localhost:8010/agents/top-free-gigs?limit=${limit}`);
  const data = await response.json();
  return data.projects;
}

getTopGigs(3).then(projects => {
  projects.forEach(project => {
    console.log(`${project.title} (Score: ${project.score})`);
  });
});
```

---

## Changelog

### v0.2.0
- Added intelligent job-type filtering
- Improved proposal generation with contextual responses
- Fixed keyword matching with word boundaries
- Added minimum score threshold filtering
- Enhanced scoring explanation clarity

### v0.1.0
- Initial release with basic scoring and collection

---

## Support

For issues or questions, please:
1. Check the main [README.md](README.md)
2. Review project [issues](https://github.com/your-repo/issues)
3. Contact the maintainer
