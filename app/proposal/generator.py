from app.database.models import FreelanceProject


def generate_proposal(project: FreelanceProject) -> str:
    title = project.title or "this project"
    skills = project.skills or "Python, FastAPI, automation, and backend development"

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
