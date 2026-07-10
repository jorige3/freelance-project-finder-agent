import feedparser

from app.collectors.base import BaseCollector, CollectedProject


class WeWorkRemotelyCollector(BaseCollector):
    name = "WeWorkRemotely"
    feed_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

    def collect(self) -> list[CollectedProject]:
        feed = feedparser.parse(self.feed_url)

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
                    opportunity_type="remote_job",
                )
            )

        return projects[:25]
