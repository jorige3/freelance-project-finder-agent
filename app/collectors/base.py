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


class BaseCollector(ABC):
    name: str

    @abstractmethod
    def collect(self) -> list[CollectedProject]:
        """Collect freelance projects from one source."""
        raise NotImplementedError
