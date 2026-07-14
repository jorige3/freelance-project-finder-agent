from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.collectors.manager import CollectorManager
from app.database.models import FreelanceProject
from app.database.session import Base, SessionLocal, engine
from app.collectors.base import CollectedProject
from app.ranking.scorer import explain_score_project, score_db_project
from app.proposal.generator import generate_proposal

from app.agents.coordinator import CoordinatorAgent
from datetime import datetime

from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Freelance Project Finder AI Agent",
    version="0.8.0",
    description="AI agent to collect, rank, and recommend freelance projects.",
    lifespan=lifespan,
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
        "version": "0.8.0",
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
    projects = db.query(FreelanceProject).all()
    for project in projects:
        project.score = score_db_project(project)
    
    projects.sort(key=lambda p: p.score, reverse=True)

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
            "is_free_to_apply": project.is_free_to_apply,
            "apply_cost": project.apply_cost,
            "opportunity_type": project.opportunity_type,
        }
        for project in projects
    ]


@app.post("/collect")
async def collect_projects(db: Session = Depends(get_db)):
    manager = CollectorManager()
    return await manager.collect_all(db)


@app.get("/projects/{project_id}/score")
def explain_project_score(project_id: int, db: Session = Depends(get_db)):
    project = (
        db.query(FreelanceProject)
        .filter(FreelanceProject.id == project_id)
        .first()
    )

    if not project:
        return {"error": "Project not found"}

    collected_project = CollectedProject.from_orm(project)

    result = explain_score_project(collected_project)

    return {
        "id": project.id,
        "title": project.title,
        "platform": project.platform,
        "stored_score": project.score,
        "calculated_score": result.score,
        "reasons": result.reasons,
    }


@app.get("/projects/{project_id}/proposal")
def get_proposal(project_id: int, db: Session = Depends(get_db)):
    project = (
        db.query(FreelanceProject)
        .filter(FreelanceProject.id == project_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Load needed attributes into memory, expunge, and close db session
    _ = (project.title, project.description, project.skills, project.budget)
    db.expunge(project)
    db.close()

    # Generate proposal without holding database session open
    proposal_text = generate_proposal(project)

    # Save to database in a short, separate transaction
    new_db = SessionLocal()
    try:
        db_project = (
            new_db.query(FreelanceProject)
            .filter(FreelanceProject.id == project_id)
            .first()
        )
        if db_project:
            db_project.proposal_text = proposal_text
            db_project.proposal_status = "generated"
            db_project.proposal_generated_at = datetime.utcnow()
            new_db.commit()
    finally:
        new_db.close()

    return {
        "id": project.id,
        "title": project.title,
        "platform": project.platform,
        "proposal": proposal_text,
        "proposal_status": "generated",
    }



@app.get("/agents/top-free-gigs")
def top_free_gigs(
    limit: int = 5,
    db: Session = Depends(get_db),
):
    coordinator = CoordinatorAgent()

    return {
        "agent": coordinator.name,
        "total": limit,
        "projects": coordinator.get_top_free_gigs(db, limit),
    }
    
class ApplicationUpdate(BaseModel):
    status: str
    notes: str | None = None
       
VALID_APPLICATION_STATUSES = {
    "saved",
    "proposal_ready",
    "applied",
    "interview",
    "offer",
    "completed",
    "rejected",
}


@app.patch("/projects/{project_id}/application")
def update_application(
    project_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(FreelanceProject)
        .filter(FreelanceProject.id == project_id)
        .first()
    )

    if not project:
        return {"error": "Project not found"}

    if payload.status not in VALID_APPLICATION_STATUSES:
        return {
            "error": "Invalid application status",
            "allowed_statuses": sorted(VALID_APPLICATION_STATUSES),
        }

    project.application_status = payload.status
    project.notes = payload.notes

    if payload.status == "applied" and project.applied_at is None:
        project.applied_at = datetime.utcnow()

    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "title": project.title,
        "application_status": project.application_status,
        "applied_at": project.applied_at,
        "notes": project.notes,
    }


@app.get("/projects/{project_id}/application")
def get_application(project_id: int, db: Session = Depends(get_db)):
    project = (
        db.query(FreelanceProject)
        .filter(FreelanceProject.id == project_id)
        .first()
    )

    if not project:
        return {"error": "Project not found"}

    return {
        "id": project.id,
        "title": project.title,
        "application_status": project.application_status,
        "applied_at": project.applied_at,
        "notes": project.notes,
    }