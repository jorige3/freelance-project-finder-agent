import pandas as pd

FREE_VALUES = {"yes", "true", "free", "free_to_apply"}
PAID_VALUES = {"no", "false", "paid"}


def score_badge(score):
    if pd.isna(score):
        return "⚪ Unknown"

    try:
        score_value = int(score)
    except (TypeError, ValueError):
        return "⚪ Unknown"

    if score_value >= 80:
        return f"🟢 {score_value}"
    if score_value >= 60:
        return f"🟡 {score_value}"
    return f"🔴 {score_value}"


def is_free_to_apply(value):
    return str(value).strip().lower() in FREE_VALUES


def free_to_apply_badge(value):
    normalized_value = str(value).strip().lower()
    if normalized_value in FREE_VALUES:
        return "🆓 Free to apply"
    if normalized_value in PAID_VALUES:
        return "💰 Paid"
    return "❓ Unknown"
