from app.collectors.base import CollectedProject

EXCLUDED_TITLE_KEYWORDS = [
    "senior",
    "sr.",
    "sr ",
    "staff",
    "principal",
    "lead ",
    "director",
    "head of",
    "vp ",
    "chief",
    "manager",
    "architect",
    "executive",
]


def is_excluded(project: CollectedProject) -> bool:
    if project.opportunity_type == "freelance":
        return False

    title_lower = project.title.lower()
    return any(keyword in title_lower for keyword in EXCLUDED_TITLE_KEYWORDS)
