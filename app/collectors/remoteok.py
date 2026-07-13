import httpx

from app.collectors.base import BaseCollector, CollectedProject
from app.collectors.opportunity_type import detect_opportunity_type


class RemoteOKCollector(BaseCollector):
    name = "RemoteOK"
    api_url = "https://remoteok.com/api"

    def collect(self) -> list[CollectedProject]:
        headers = {
            "User-Agent": "freelance-project-finder-agent/0.1"
        }

        response = httpx.get(self.api_url, headers=headers, timeout=30.0)
        response.raise_for_status()

        data = response.json()

        projects: list[CollectedProject] = []

        for item in data:
            if not isinstance(item, dict):
                continue

            title = item.get("position") or item.get("title")
            company = item.get("company", "")
            url = item.get("url") or item.get("apply_url")

            if not title or not url:
                continue

            tags = item.get("tags") or []
            skills = ", ".join(tags) if isinstance(tags, list) else str(tags)

            salary_min = item.get("salary_min")
            salary_max = item.get("salary_max")

            budget = ""
            if salary_min or salary_max:
                budget = f"${salary_min or 0} - ${salary_max or 0}"

            description = f"Remote job at {company}".strip()

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
                    opportunity_type=detect_opportunity_type(title, description),
                )
            )

        return projects[:25]
