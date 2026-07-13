import re
from dataclasses import dataclass

from app.collectors.base import CollectedProject


@dataclass
class ScoreResult:
    score: int
    reasons: list[str]


SKILL_WEIGHTS = {
    "python": 25, "fastapi": 25, "api": 15, "automation": 20, "ai": 20,
    "machine learning": 20, "data science": 15, "docker": 15, "devops": 15,
    "linux": 10, "sqlite": 10, "backend": 15, "cloud": 10, "azure": 10, "aws": 10,
}
EASY_KEYWORDS = {"simple", "small", "easy", "junior", "entry level", "beginner", "script", "automation"}
NEGATIVE_KEYWORDS = {"senior": -10, "lead": -15, "manager": -20, "director": -25, "casino": -30, "gambling": -30}

# Freelance gigs are the actual target; full-time remote jobs are secondary
# even when skills overlap.
OPPORTUNITY_TYPE_MULTIPLIER = {"freelance": 1.0, "remote_job": 0.6}


def _parsed_tags(skills_field: str) -> set[str]:
    return {t.strip().lower() for t in (skills_field or "").split(",") if t.strip()}


def keyword_found(keyword: str, text: str) -> bool:
    return re.search(r"\b" + re.escape(keyword) + r"\b", text) is not None


def explain_score_project(project: CollectedProject) -> ScoreResult:
    title_desc = " ".join([project.title or "", project.description or ""]).lower()
    tags = _parsed_tags(project.skills or "")
    tag_count = max(len(tags), 1)
    # Dilute skill-match reward when the tag list is spammy (>8 tags) —
    # a match among 3 tags is a much stronger signal than among 40.
    dilution = 1.0 if tag_count <= 8 else 8 / tag_count

    score = 20
    reasons = ["Base score +20"]

    for keyword, points in SKILL_WEIGHTS.items():
        if keyword in tags or keyword_found(keyword, title_desc):
            adj = round(points * dilution)
            score += adj
            reasons.append(f"Matched skill '{keyword}' +{adj}" + ("" if dilution == 1.0 else f" (diluted x{dilution:.2f})"))

    for keyword in EASY_KEYWORDS:
        if keyword_found(keyword, title_desc):
            score += 5
            reasons.append(f"Beginner-friendly keyword '{keyword}' +5")

    for keyword, points in NEGATIVE_KEYWORDS.items():
        if keyword_found(keyword, title_desc):
            score += points
            reasons.append(f"Penalty keyword '{keyword}' {points:+d}")

    opp_type = project.opportunity_type or "remote_job"
    multiplier = OPPORTUNITY_TYPE_MULTIPLIER.get(opp_type, 0.6)
    scaled = round(score * multiplier)
    if multiplier != 1.0:
        reasons.append(f"Opportunity type '{opp_type}' scaled x{multiplier} -> {scaled}")

    final = max(0, min(scaled, 100))
    if final != scaled:
        reasons.append(f"Score capped from {scaled} to {final}")
    return ScoreResult(score=final, reasons=reasons)


def score_project(project: CollectedProject) -> int:
    return explain_score_project(project).score


def score_db_project(project) -> int:
    collected = CollectedProject(
        title=project.title,
        platform=project.platform,
        url=project.url or "",
        description=project.description or "",
        budget=project.budget or "",
        skills=project.skills or "",
        difficulty=project.difficulty or "unknown",
        score=0,
        is_free_to_apply=getattr(project, "is_free_to_apply", "unknown") or "unknown",
        apply_cost=getattr(project, "apply_cost", "unknown") or "unknown",
        opportunity_type=getattr(project, "opportunity_type", "remote_job") or "remote_job",
    )
    return score_project(collected)

