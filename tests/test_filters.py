from app.collectors.base import CollectedProject
from app.collectors.filters import is_excluded, EXCLUDED_TITLE_KEYWORDS

def test_is_excluded_senior_regardless_of_opportunity_type():
    p_freelance = CollectedProject(
        title="Senior Software Engineer",
        platform="Test",
        url="https://example.com/1",
        opportunity_type="freelance"
    )
    p_remote = CollectedProject(
        title="Senior Software Engineer",
        platform="Test",
        url="https://example.com/1",
        opportunity_type="remote_job"
    )
    assert is_excluded(p_freelance) is True
    assert is_excluded(p_remote) is True

def test_is_excluded_relevant_allowed():
    p = CollectedProject(
        title="Python script for file automation",
        platform="Test",
        url="https://example.com/1",
        opportunity_type="freelance"
    )
    assert is_excluded(p) is False

def test_excluded_keywords():
    for keyword in EXCLUDED_TITLE_KEYWORDS:
        title = f"test {keyword} test"
        p = CollectedProject(
            title=title,
            platform="Test",
            url="https://example.com/1",
            opportunity_type="remote_job"
        )
        assert is_excluded(p) is True, f"Keyword '{keyword}' did not trigger exclusion"
