from app.database.models import FreelanceProject
from app.proposal.generator import is_tech_job

# Minimum score threshold for recommendations
MIN_SCORE_THRESHOLD = 50


class FilterAgent:
    name = "FilterAgent"

    def free_to_apply(self, projects: list[FreelanceProject]) -> list[FreelanceProject]:
        """Filter for free-to-apply projects."""
        return [
            project
            for project in projects
            if project.is_free_to_apply == "yes"
        ]
    
    def relevant_jobs(self, projects: list[FreelanceProject]) -> list[FreelanceProject]:
        """Filter for tech jobs with minimum score threshold."""
        return [
            project
            for project in projects
            if is_tech_job(project) and project.score >= MIN_SCORE_THRESHOLD
        ]
