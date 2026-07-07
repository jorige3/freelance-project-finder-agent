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

class BaseCollector(ABC):
    name: str

    @abstractmethod
    def collect(self) -> list[CollectedProject]:
        """Collect freelance projects from one source."""
        raise NotImplementedError
