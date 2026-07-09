import re
from app.database.models import FreelanceProject

# Tech-related keywords to identify development roles
TECH_KEYWORDS = {
    "python", "java", "javascript", "typescript", "react", "vue", "angular",
    "fastapi", "django", "flask", "nodejs", "backend", "frontend", "fullstack",
    "api", "database", "sql", "mongodb", "docker", "kubernetes", "devops",
    "machine learning", "artificial intelligence", "data science", "automation", "script", "coding",
    "development", "engineer", "developer", "programmer", "software", "web dev", "web development"
}


def is_tech_job(project: FreelanceProject) -> bool:
    """Determine if a project is a tech/development job using word boundaries."""
    text = " ".join([
        project.title or "",
        project.description or "",
        project.skills or ""
    ]).lower()
    
    for keyword in TECH_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            return True
    return False


def generate_proposal(project: FreelanceProject) -> str:
    title = project.title or "this project"
    skills = project.skills or "Python, FastAPI, automation, and backend development"
    
    # Check if it's a tech job
    if not is_tech_job(project):
        return f"""Hello,

Thank you for the opportunity with "{title}".

While I appreciate the role, my expertise is primarily in software development and technical projects (Python, APIs, automation, backend systems). This role seems focused on {skills.lower()}, which is outside my core specialization.

I'd recommend finding a specialist in that area for the best results.

Best regards,
Kishore Kumar Jorige
"""
    
    # Generate tech-focused proposal
    return f"""Hello,

I can help you with "{title}".

I have hands-on experience with {skills}. I can understand your requirement, build a clean working solution, and provide simple setup instructions so you can run it easily.

My approach:
1. Review the requirement clearly.
2. Build a small working version first.
3. Test it properly.
4. Improve it based on your feedback.
5. Deliver clean code with basic documentation.

I focus on practical, reliable, and easy-to-maintain solutions.

Thank you,
Kishore Kumar Jorige
"""
