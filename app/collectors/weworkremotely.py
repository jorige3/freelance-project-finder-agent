import feedparser
import httpx

from app.collectors.base import BaseCollector, CollectedProject
from app.collectors.opportunity_type import detect_opportunity_type


class WeWorkRemotelyCollector(BaseCollector):
    name = "WeWorkRemotely"
    feed_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

    async def collect(self) -> list[CollectedProject]:
        headers = {
            "User-Agent": "freelance-project-finder-agent/0.1"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.feed_url, headers=headers, timeout=30.0)
        response.raise_for_status()

        feed = feedparser.parse(response.content)

        projects: list[CollectedProject] = []

        for entry in feed.entries:
            title = entry.get("title")
            url = entry.get("link")

            if not title or not url:
                continue

            description = entry.get("summary", "") or ""

            projects.append(
                CollectedProject(
                    title=title,
                    platform=self.name,
                    url=url,
                    description=description[:500],
                    budget="",
                    skills="",
                    difficulty="unknown",
                    score=50,
                    is_free_to_apply="yes",
                    apply_cost="free",
                    opportunity_type=detect_opportunity_type(title, description),
                )
            )

        return projects[:25]
