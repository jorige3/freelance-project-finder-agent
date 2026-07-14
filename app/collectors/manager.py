from sqlalchemy.orm import Session

from app.collectors.base import BaseCollector
from app.collectors.filters import is_excluded
from app.collectors.mock_collector import MockCollector
from app.collectors.remoteok import RemoteOKCollector
from app.collectors.remotive import RemotiveCollector
from app.collectors.weworkremotely import WeWorkRemotelyCollector
from app.database.models import FreelanceProject
from app.ranking.scorer import score_project


class CollectorManager:
    def __init__(self):
        self.collectors: list[BaseCollector] = [
            MockCollector(),
            RemoteOKCollector(),
            RemotiveCollector(),
            WeWorkRemotelyCollector(),
        ]

    async def collect_all(self, db: Session) -> dict:
        import asyncio
        inserted = 0
        duplicates = 0
        filtered_out = 0
        errors: list[str] = []

        # Fetch all collectors concurrently
        tasks = [collector.collect() for collector in self.collectors]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_collected_projects = []
        for collector, result in zip(self.collectors, results):
            if isinstance(result, Exception):
                errors.append(f"{collector.name}: {result}")
            else:
                all_collected_projects.extend(result)

        total_found = len(all_collected_projects)

        # Filter out excluded titles first
        valid_projects = []
        for project in all_collected_projects:
            if is_excluded(project):
                filtered_out += 1
            else:
                valid_projects.append(project)

        # Batch query existing URLs to prevent N+1 query problem
        if valid_projects:
            urls = {p.url for p in valid_projects if p.url}
            existing_urls = {
                row[0]
                for row in db.query(FreelanceProject.url)
                .filter(FreelanceProject.url.in_(list(urls)))
                .all()
            }
        else:
            existing_urls = set()

        # Insert new projects
        for project in valid_projects:
            if project.url in existing_urls:
                duplicates += 1
                continue

            existing_urls.add(project.url)

            db_project = FreelanceProject(
                title=project.title,
                platform=project.platform,
                url=project.url,
                description=project.description,
                budget=project.budget,
                skills=project.skills,
                difficulty=project.difficulty,
                score=score_project(project),
                is_free_to_apply=project.is_free_to_apply,
                apply_cost=project.apply_cost,
                opportunity_type=project.opportunity_type,
            )
            db.add(db_project)
            inserted += 1

        db.commit()

        return {
            "status": "success",
            "total_found": total_found,
            "inserted": inserted,
            "duplicates_skipped": duplicates,
            "filtered_out": filtered_out,
            "errors": errors,
        }
