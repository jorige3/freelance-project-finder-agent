from sqlalchemy.orm import Session

from app.collectors.manager import CollectorManager


class CollectorAgent:
    name = "CollectorAgent"

    async def run(self, db: Session) -> dict:
        manager = CollectorManager()
        return await manager.collect_all(db)
