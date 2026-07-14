from dashboard.helpers import score_badge, is_free_to_apply, free_to_apply_badge

def test_score_badge():
    assert score_badge(85) == "🟢 85"
    assert score_badge(70) == "🟡 70"
    assert score_badge(50) == "🔴 50"
    assert score_badge(None) == "⚪ Unknown"
    assert score_badge("invalid") == "⚪ Unknown"

def test_is_free_to_apply():
    assert is_free_to_apply("yes") is True
    assert is_free_to_apply("FREE_TO_APPLY") is True
    assert is_free_to_apply("no") is False
    assert is_free_to_apply("paid") is False

def test_free_to_apply_badge():
    assert free_to_apply_badge("yes") == "🆓 Free to apply"
    assert free_to_apply_badge("paid") == "💰 Paid"
    assert free_to_apply_badge("unknown") == "❓ Unknown"
