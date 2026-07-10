import httpx

from app.collectors.base import BaseCollector, CollectedProject


class RemotiveCollector(BaseCollector):
    name = "Remotive"
    api_url = "https://remotive.com/api/remote-jobs"

    def collect(self) -> list[CollectedProject]:
        headers = {
            "User-Agent": "freelance-project-finder-agent/0.1"
        }

        response = httpx.get(self.api_url, headers=headers, timeout=30.0)
        response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])

        projects: list[CollectedProject] = []

        for item in jobs:
            if not isinstance(item, dict):
                continue

            title = item.get("title")
            url = item.get("url")

            if not title or not url:
                continue

            tags = item.get("tags") or []
            skills = ", ".join(tags) if isinstance(tags, list) else str(tags)

            salary = item.get("salary") or ""
            budget = salary.strip()

            description = item.get("description", "") or ""
            description = description[:500]

            projects.append(
                CollectedProject(
                    title=title,
                    platform=self.name,
                    url=url,
                    description=description,
                    budget=budget,
                    skills=skills,
                    difficulty="unknown",
                    score=50,
                    is_free_to_apply="yes",
                    apply_cost="free",
                    opportunity_type="remote_job",
                )
            )

        return projects[:25]
