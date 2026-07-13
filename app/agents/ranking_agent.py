from app.collectors.base import CollectedProject
from app.database.models import FreelanceProject
from app.ranking.scorer import explain_score_project


class RankingAgent:
    name = "RankingAgent"

    def explain(self, project: FreelanceProject) -> dict:
        collected_project = CollectedProject.from_orm(project)

        result = explain_score_project(collected_project)

        return {
            "score": result.score,
            "reasons": result.reasons,
        }
