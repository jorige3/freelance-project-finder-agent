from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CollectedProject:
    title: str
    platform: str
    url: str
    description: str = ""
    budget: str = ""
    skills: str = ""
    difficulty: str = "unknown"
    score: int = 0
    is_free_to_apply: str = "unknown"
    apply_cost: str = "unknown"
    opportunity_type: str = "remote_job"

    @classmethod
    def from_orm(cls, project) -> "CollectedProject":
        return cls(
            title=getattr(project, "title", "") or "",
            platform=getattr(project, "platform", "") or "",
            url=getattr(project, "url", "") or "",
            description=getattr(project, "description", "") or "",
            budget=getattr(project, "budget", "") or "",
            skills=getattr(project, "skills", "") or "",
            difficulty=getattr(project, "difficulty", "unknown") or "unknown",
            score=getattr(project, "score", 0) or 0,
            is_free_to_apply=getattr(project, "is_free_to_apply", "unknown") or "unknown",
            apply_cost=getattr(project, "apply_cost", "unknown") or "unknown",
            opportunity_type=getattr(project, "opportunity_type", "remote_job") or "remote_job",
        )

class BaseCollector(ABC):
    name: str

    @abstractmethod
    async def collect(self) -> list[CollectedProject]:
        """Collect freelance projects from one source asynchronously."""
        raise NotImplementedError
