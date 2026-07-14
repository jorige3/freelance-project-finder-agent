from unittest.mock import patch
from app.database.models import FreelanceProject
from app.proposal.generator import generate_proposal, _static_tech_proposal
from app.proposal.ollama_client import OllamaUnavailableError

def test_proposal_fallback_on_ollama_unavailable():
    project = FreelanceProject(
        title="FastAPI Integration",
        description="Need python developer to integrate api",
        skills="Python, FastAPI",
        budget="$500"
    )
    
    with patch("app.proposal.generator.generate_with_ollama") as mock_generate:
        mock_generate.side_effect = OllamaUnavailableError("Ollama is offline")
        
        proposal = generate_proposal(project)
        
        # Should fall back to static tech proposal
        expected = _static_tech_proposal(project.title, project.skills)
        assert proposal == expected
