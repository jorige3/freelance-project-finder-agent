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

    def collect_all(self, db: Session) -> dict:
        total_found = 0
        inserted = 0
        duplicates = 0
        filtered_out = 0
        errors: list[str] = []

        for collector in self.collectors:
            try:
                projects = collector.collect()
            except Exception as exc:
                errors.append(f"{collector.name}: {exc}")
                continue

            total_found += len(projects)

            for project in projects:
                if is_excluded(project):
                    filtered_out += 1
                    continue

                existing = (
                    db.query(FreelanceProject)
                    .filter(FreelanceProject.url == project.url)
                    .first()
                )

                if existing:
                    duplicates += 1
                    continue

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
