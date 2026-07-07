from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.collectors.manager import CollectorManager
from app.database.models import FreelanceProject
from app.database.session import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Freelance Project Finder AI Agent",
    version="0.2.0",
    description="AI agent to collect, rank, and recommend freelance projects.",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "status": "running",
        "project": "Freelance Project Finder AI Agent",
        "version": "0.2.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/projects/seed")
def seed_projects(db: Session = Depends(get_db)):
    sample_projects = [
        FreelanceProject(
            title="Build a Python automation script",
            platform="Sample",
            url="https://example.com/python-automation",
            description="Need a Python script to automate CSV cleanup and email reports.",
            budget="$150",
            skills="Python, Automation, CSV",
            difficulty="easy",
            score=85,
        ),
        FreelanceProject(
            title="FastAPI backend for small dashboard",
            platform="Sample",
            url="https://example.com/fastapi-dashboard",
            description="Create REST APIs for a simple analytics dashboard.",
            budget="$300",
            skills="Python, FastAPI, SQLite",
            difficulty="medium",
            score=90,
        ),
    ]

    db.add_all(sample_projects)
    db.commit()

    return {"inserted": len(sample_projects)}


@app.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(FreelanceProject).order_by(FreelanceProject.score.desc()).all()

    return [
        {
            "id": project.id,
            "title": project.title,
            "platform": project.platform,
            "budget": project.budget,
            "skills": project.skills,
            "difficulty": project.difficulty,
            "score": project.score,
            "url": project.url,
        }
        for project in projects
    ]


@app.post("/collect")
def collect_projects(db: Session = Depends(get_db)):
    manager = CollectorManager()
    return manager.collect_all(db)
