from app.collectors.base import CollectedProject
from app.database.models import FreelanceProject
from app.ranking.scorer import explain_score_project


class RankingAgent:
    name = "RankingAgent"

    def explain(self, project: FreelanceProject) -> dict:
        collected_project = CollectedProject(
            title=project.title,
            platform=project.platform,
            url=project.url or "",
            description=project.description or "",
            budget=project.budget or "",
            skills=project.skills or "",
            difficulty=project.difficulty or "unknown",
            score=project.score or 0,
            is_free_to_apply=project.is_free_to_apply or "unknown",
            apply_cost=project.apply_cost or "unknown",
            opportunity_type=project.opportunity_type or "unknown",
        )

        result = explain_score_project(collected_project)

        return {
            "score": result.score,
            "reasons": result.reasons,
        }
