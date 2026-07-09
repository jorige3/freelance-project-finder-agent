from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database.session import Base


class FreelanceProject(Base):
    __tablename__ = "freelance_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    platform = Column(String(100), nullable=False)
    url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    budget = Column(String(100), nullable=True)
    skills = Column(Text, nullable=True)
    difficulty = Column(String(50), default="unknown")
    score = Column(Integer, default=0)
    status = Column(String(50), default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_free_to_apply = Column(String(10), default="unknown")
    apply_cost = Column(String(50), default="unknown")
    opportunity_type = Column(String(50), default="remote_job")
