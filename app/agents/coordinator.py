from sqlalchemy.orm import Session

from app.agents.collector_agent import CollectorAgent
from app.agents.filter_agent import FilterAgent
from app.agents.proposal_agent import ProposalAgent
from app.agents.ranking_agent import RankingAgent
from app.database.models import FreelanceProject


class CoordinatorAgent:
    name = "CoordinatorAgent"

    def __init__(self):
        self.collector_agent = CollectorAgent()
        self.filter_agent = FilterAgent()
        self.ranking_agent = RankingAgent()
        self.proposal_agent = ProposalAgent()

    def collect(self, db: Session) -> dict:
        return self.collector_agent.run(db)

    def get_top_free_gigs(self, db: Session, limit: int = 5) -> list[dict]:
        projects = (
            db.query(FreelanceProject)
            .order_by(FreelanceProject.score.desc())
            .all()
        )

        free_projects = self.filter_agent.free_to_apply(projects)
        relevant_projects = self.filter_agent.relevant_jobs(free_projects)

        top_projects = relevant_projects[:limit]

        return [
            {
                "id": project.id,
                "title": project.title,
                "platform": project.platform,
                "score": project.score,
                "budget": project.budget,
                "skills": project.skills,
                "url": project.url,
                "explanation": self.ranking_agent.explain(project),
                "proposal": self.proposal_agent.generate(project),
            }
            for project in top_projects
        ]
