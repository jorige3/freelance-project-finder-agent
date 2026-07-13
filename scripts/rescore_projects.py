import sys
import os

# Adjust path to import app correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.database.models import FreelanceProject
from app.ranking.scorer import score_db_project

def rescore_all():
    db = SessionLocal()
    try:
        projects = db.query(FreelanceProject).all()
        print(f"Rescoring {len(projects)} projects...")
        updated = 0
        for project in projects:
            old_score = project.score
            new_score = score_db_project(project)
            if old_score != new_score:
                project.score = new_score
                updated += 1
                print(f"Project ID {project.id} ('{project.title}'): score updated from {old_score} to {new_score}")
        db.commit()
        print(f"Successfully updated score for {updated} projects.")
    finally:
        db.close()

if __name__ == "__main__":
    rescore_all()
