from sqlalchemy.orm import Session

from app.collectors.base import BaseCollector
from app.collectors.mock_collector import MockCollector
from app.collectors.remoteok import RemoteOKCollector
from app.database.models import FreelanceProject
from app.ranking.scorer import score_project
from app.ranking.scorer import score_project
from app.ranking.scorer import score_project


class CollectorManager:
    def __init__(self):
        self.collectors: list[BaseCollector] = [
            MockCollector(),
            RemoteOKCollector(),
        ]

    def collect_all(self, db: Session) -> dict:
        total_found = 0
        inserted = 0
        duplicates = 0

        for collector in self.collectors:
            projects = collector.collect()
            total_found += len(projects)

            for project in projects:
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
                )
                db.add(db_project)
                inserted += 1

        db.commit()

        return {
            "status": "success",
            "total_found": total_found,
            "inserted": inserted,
            "duplicates_skipped": duplicates,
        }
