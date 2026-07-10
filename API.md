# API Documentation

## Base URL

```text
http://localhost:8010
```

## Overview

This document describes the current FastAPI endpoints exposed by the Freelance Project Finder agent.

---

## Endpoints

### Health & Status

#### GET /
Returns basic service metadata.

Response:
```json
{
  "status": "running",
  "project": "Freelance Project Finder AI Agent",
  "version": "0.2.0"
}
```

#### GET /health
Returns a simple health check response.

Response:
```json
{
  "status": "healthy"
}
```

---

### Projects

#### POST /projects/seed
Seeds the database with sample projects.

Response:
```json
{
  "inserted": 2
}
```

#### GET /projects
Lists stored projects sorted by score, highest first.

Response:
```json
[
  {
    "id": 1,
    "title": "Build a Python automation script",
    "platform": "Sample",
    "budget": "$150",
    "skills": "Python, Automation, CSV",
    "difficulty": "easy",
    "score": 85,
    "url": "https://example.com/python-automation",
    "is_free_to_apply": null,
    "apply_cost": null,
    "opportunity_type": null
  }
]
```

#### POST /collect
Triggers the collector manager to gather opportunities.

Response:
```json
{
  "status": "success",
  "total_found": 10,
  "inserted": 3,
  "duplicates_skipped": 7
}
```

---

### Scoring & Proposal

#### GET /projects/{project_id}/score
Returns the stored score along with the dynamically calculated explanation.

Path parameters:
- `project_id` (int, required)

Response:
```json
{
  "id": 1,
  "title": "Build a Python automation script",
  "platform": "Sample",
  "stored_score": 85,
  "calculated_score": 85,
  "reasons": [
    "Matched skill 'python' +25",
    "Matched skill 'automation' +20"
  ]
}
```

#### GET /projects/{project_id}/proposal
Generates a proposal for a specific project and stores it in the database.

Path parameters:
- `project_id` (int, required)

Response:
```json
{
  "id": 1,
  "title": "Build a Python automation script",
  "platform": "Sample",
  "proposal": "Hello, ...",
  "proposal_status": "generated"
}
```

---

### Application Tracking

#### GET /projects/{project_id}/application
Returns the current application status for a project.

Response:
```json
{
  "id": 1,
  "title": "Build a Python automation script",
  "application_status": "saved",
  "applied_at": null,
  "notes": null
}
```

#### PATCH /projects/{project_id}/application
Updates the application workflow state for a project.

Request body:
```json
{
  "status": "applied",
  "notes": "Submitted my proposal today."
}
```

Allowed values:
- `saved`
- `proposal_ready`
- `applied`
- `interview`
- `offer`
- `completed`
- `rejected`

Response:
```json
{
  "id": 1,
  "title": "Build a Python automation script",
  "application_status": "applied",
  "applied_at": "2026-07-10T12:00:00",
  "notes": "Submitted my proposal today."
}
```

---

### Agent Endpoints

#### GET /agents/top-free-gigs
Returns the top recommended free-to-apply opportunities from the coordinator agent.

Query parameters:
- `limit` (int, default: 5)

Response:
```json
{
  "agent": "CoordinatorAgent",
  "total": 5,
  "projects": []
}
```

---

## Error Responses

### 404 - Not Found
```json
{
  "error": "Project not found"
}
```

### 400 - Bad Request
```json
{
  "error": "Invalid application status",
  "allowed_statuses": [
    "applied",
    "completed",
    "interview",
    "offer",
    "proposal_ready",
    "rejected",
    "saved"
  ]
}
```
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
2. Review project [issues](https://github.com/jorige3/issues)
3. Contact the maintainer
