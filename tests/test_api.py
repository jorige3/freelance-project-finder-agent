import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///./test_freelance_projects.db"

from app.database.session import Base, engine
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def remove_test_db_file():
    yield
    for suffix in ["", "-wal", "-shm"]:
        path = f"./test_freelance_projects.db{suffix}"
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "running"
        assert response.json()["version"] == "0.8.0"

def test_seed_and_list_projects():
    with TestClient(app) as client:
        # Seed
        response = client.post("/projects/seed")
        assert response.status_code == 200
        assert "inserted" in response.json()

        # List
        response = client.get("/projects")
        assert response.status_code == 200
        projects = response.json()
        assert len(projects) >= 2

def test_application_tracker_endpoints():
    with TestClient(app) as client:
        # Seed first to get valid ID
        client.post("/projects/seed")
        
        projects_response = client.get("/projects")
        assert projects_response.status_code == 200
        project_id = projects_response.json()[0]["id"]

        # Get application status
        get_resp = client.get(f"/projects/{project_id}/application")
        assert get_resp.status_code == 200
        assert get_resp.json()["application_status"] == "saved"

        # Update application status
        patch_resp = client.patch(
            f"/projects/{project_id}/application",
            json={"status": "applied", "notes": "Sent a proposal"}
        )
        assert patch_resp.status_code == 200
        assert patch_resp.json()["application_status"] == "applied"
        assert patch_resp.json()["notes"] == "Sent a proposal"
