from sqlalchemy.orm import Session

from app.collectors.manager import CollectorManager


class CollectorAgent:
    name = "CollectorAgent"

    def run(self, db: Session) -> dict:
        manager = CollectorManager()
        return manager.collect_all(db)
