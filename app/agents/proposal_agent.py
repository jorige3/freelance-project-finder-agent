from app.database.models import FreelanceProject
from app.proposal.generator import generate_proposal


class ProposalAgent:
    name = "ProposalAgent"

    def generate(self, project: FreelanceProject) -> str:
        return generate_proposal(project)
