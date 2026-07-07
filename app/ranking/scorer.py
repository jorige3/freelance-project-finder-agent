from dataclasses import dataclass

from app.collectors.base import CollectedProject


@dataclass
class ScoreResult:
    score: int
    reasons: list[str]


SKILL_WEIGHTS = {
    "python": 25,
    "fastapi": 25,
    "api": 15,
    "automation": 20,
    "ai": 20,
    "machine learning": 20,
    "data science": 15,
    "docker": 15,
    "devops": 15,
    "linux": 10,
    "sqlite": 10,
    "backend": 15,
    "cloud": 10,
    "azure": 10,
    "aws": 10,
}

EASY_KEYWORDS = {
    "simple",
    "small",
    "easy",
    "junior",
    "entry level",
    "beginner",
    "script",
    "automation",
}

NEGATIVE_KEYWORDS = {
    "senior": -10,
    "lead": -15,
    "manager": -20,
    "director": -25,
    "casino": -30,
    "gambling": -30,
}


def explain_score_project(project: CollectedProject) -> ScoreResult:
    text = " ".join(
        [
            project.title or "",
            project.description or "",
            project.skills or "",
            project.budget or "",
        ]
    ).lower()

    score = 30
    reasons = ["Base score +30"]

    for keyword, points in SKILL_WEIGHTS.items():
        if keyword in text:
            score += points
            reasons.append(f"Matched skill '{keyword}' +{points}")

    for keyword in EASY_KEYWORDS:
        if keyword in text:
            score += 5
            reasons.append(f"Beginner-friendly keyword '{keyword}' +5")

    for keyword, points in NEGATIVE_KEYWORDS.items():
        if keyword in text:
            score += points
            reasons.append(f"Penalty keyword '{keyword}' {points}")

    final_score = max(0, min(score, 100))

    if final_score != score:
        reasons.append(f"Score capped from {score} to {final_score}")

    return ScoreResult(score=final_score, reasons=reasons)


def score_project(project: CollectedProject) -> int:
    return explain_score_project(project).score
