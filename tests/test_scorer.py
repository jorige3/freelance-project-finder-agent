from app.collectors.base import CollectedProject
from app.ranking.scorer import explain_score_project, score_project

def test_opportunity_type_multiplier():
    p_freelance = CollectedProject(
        title="FastAPI Developer",
        platform="Test",
        url="https://example.com/1",
        description="Looking for Python FastAPI developer",
        skills="Python, FastAPI, SQLite",
        opportunity_type="freelance"
    )
    p_remote = CollectedProject(
        title="FastAPI Developer",
        platform="Test",
        url="https://example.com/1",
        description="Looking for Python FastAPI developer",
        skills="Python, FastAPI, SQLite",
        opportunity_type="remote_job"
    )
    score_f = score_project(p_freelance)
    score_r = score_project(p_remote)
    
    assert score_f > score_r
    assert score_r == round(score_f * 0.6)

def test_tag_spam_dilution():
    p_3_tags = CollectedProject(
        title="FastAPI Developer",
        platform="Test",
        url="https://example.com/1",
        description="Looking for Python FastAPI developer",
        skills="Python, FastAPI, SQLite",
        opportunity_type="freelance"
    )
    spam_skills = "Python, FastAPI, SQLite, " + ", ".join(f"skill{i}" for i in range(32))
    p_35_tags = CollectedProject(
        title="FastAPI Developer",
        platform="Test",
        url="https://example.com/1",
        description="Looking for Python FastAPI developer",
        skills=spam_skills,
        opportunity_type="freelance"
    )
    score_3 = score_project(p_3_tags)
    score_35 = score_project(p_35_tags)
    
    assert score_3 > score_35

def test_negative_keywords():
    p_normal = CollectedProject(
        title="Python Developer",
        platform="Test",
        url="https://example.com/1",
        skills="Python",
        opportunity_type="freelance"
    )
    p_senior = CollectedProject(
        title="Senior Python Developer",
        platform="Test",
        url="https://example.com/1",
        skills="Python",
        opportunity_type="freelance"
    )
    p_manager = CollectedProject(
        title="Python Manager",
        platform="Test",
        url="https://example.com/1",
        skills="Python",
        opportunity_type="freelance"
    )
    
    score_normal = score_project(p_normal)
    score_senior = score_project(p_senior)
    score_manager = score_project(p_manager)
    
    assert score_senior < score_normal
    assert score_manager < score_normal

def test_score_clamping():
    p_low = CollectedProject(
        title="Senior Lead Manager Director Casino Gambling",
        platform="Test",
        url="https://example.com/1",
        skills="",
        opportunity_type="remote_job"
    )
    skills = "Python, FastAPI, API, automation, AI, Docker, DevOps, Linux, SQLite, Backend, Cloud, Azure, AWS"
    p_high = CollectedProject(
        title="Python FastAPI API automation AI Docker DevOps Linux SQLite Backend Cloud Azure AWS simple small easy",
        platform="Test",
        url="https://example.com/1",
        skills=skills,
        opportunity_type="freelance"
    )
    
    assert score_project(p_low) >= 0
    assert score_project(p_high) <= 100

def test_dilution_explanation_note():
    spam_skills = "Python, FastAPI, SQLite, " + ", ".join(f"skill{i}" for i in range(10))
    p_spam = CollectedProject(
        title="FastAPI Developer",
        platform="Test",
        url="https://example.com/1",
        skills=spam_skills,
        opportunity_type="freelance"
    )
    explanation = explain_score_project(p_spam)
    
    has_dilution_note = any("diluted x" in reason for reason in explanation.reasons)
    assert has_dilution_note
