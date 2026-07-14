from app.collectors.base import BaseCollector, CollectedProject


class MockCollector(BaseCollector):
    name = "Mock"

    async def collect(self) -> list[CollectedProject]:
        return [
            CollectedProject(
                title="Python script for file automation",
                platform=self.name,
                url="https://example.com/mock-python-file-automation",
                description="Create a Python script to organize files and generate reports.",
                budget="$100",
                skills="Python, Automation, Files",
                difficulty="easy",
                score=80,
                is_free_to_apply="yes",
                apply_cost="free",
                opportunity_type="freelance",
            ),
            CollectedProject(
                title="Build FastAPI CRUD backend",
                platform=self.name,
                url="https://example.com/mock-fastapi-crud",
                description="Need a simple FastAPI backend with SQLite database.",
                budget="$250",
                skills="Python, FastAPI, SQLite",
                difficulty="medium",
                score=88,
                is_free_to_apply="yes",
                apply_cost="free",
                opportunity_type="freelance",
            ),
        ]