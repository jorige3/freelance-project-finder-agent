import logging
import re

from app.database.models import FreelanceProject
from app.proposal.ollama_client import OllamaUnavailableError, generate_with_ollama

TECH_KEYWORDS = {
    "python", "java", "javascript", "typescript", "react", "vue", "angular",
    "fastapi", "django", "flask", "nodejs", "backend", "frontend", "fullstack",
    "api", "database", "sql", "mongodb", "docker", "kubernetes", "devops",
    "machine learning", "artificial intelligence", "data science", "automation", "script", "coding",
    "development", "engineer", "developer", "programmer", "software", "web dev", "web development"
}


def is_tech_job(project: FreelanceProject) -> bool:
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


def _static_tech_proposal(title: str, skills: str) -> str:
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


def _static_non_tech_proposal(title: str, skills: str) -> str:
    return f"""Hello,

Thank you for the opportunity with "{title}".

While I appreciate the role, my expertise is primarily in software development and technical projects (Python, APIs, automation, backend systems). This role seems focused on {skills.lower()}, which is outside my core specialization.

I'd recommend finding a specialist in that area for the best results.

Best regards,
Kishore Kumar Jorige
"""


def _build_llm_prompt(project: FreelanceProject, title: str, skills: str) -> str:
    description = (project.description or "").strip()
    budget = project.budget or "not specified"

    return f"""You are Kishore Kumar Jorige, a freelance Python/backend developer. Your ONLY confirmed skills are: {skills}.

Write a short freelance proposal (100-150 words) for this job listing:

Title: {title}
Budget: {budget}
Description: {description[:800]}

STRICT RULES:
- Do NOT invent, mention, or imply any past projects, clients, companies, or work history. You have no specific past projects to reference.
- Do NOT mention any skill, tool, or technology that is not explicitly listed above in "confirmed skills".
- Only reference details that are explicitly present in the job Title or Description above.
- Describe your approach/process for THIS job, not past experience.
- Plain text only. Do not use asterisks, markdown, bold, or any special formatting characters.
- Write the signature exactly once, at the very end, as: Kishore Kumar Jorige
- Output ONLY the proposal text. No preamble, no explanation, no headers.
"""


def _clean_llm_output(text: str) -> str:
    """Strip common markdown artifacts small local models tend to add."""
    cleaned = text.replace("**", "").replace("__", "")
    cleaned = cleaned.replace("---", "").replace("###", "").replace("##", "").replace("# ", "")
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    return cleaned.strip() + "\n"


def generate_proposal(project: FreelanceProject) -> str:
    title = project.title or "this project"
    skills = project.skills or "Python, FastAPI, automation, and backend development"

    if not is_tech_job(project):
        return _static_non_tech_proposal(title, skills)

    try:
        prompt = _build_llm_prompt(project, title, skills)
        raw = generate_with_ollama(prompt)
        return _clean_llm_output(raw)
    except OllamaUnavailableError as exc:
        logging.warning("Ollama proposal generation failed, using static fallback: %s", exc)
        return _static_tech_proposal(title, skills)
