import pandas as pd
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8010"


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


def free_to_apply_badge(value):
    normalized_value = str(value).strip().lower()
    if normalized_value in {"yes", "true", "free", "free_to_apply"}:
        return "🆓 Free to apply"
    if normalized_value in {"no", "false", "paid"}:
        return "💰 Paid"
    return "❓ Unknown"


def load_projects():
    return requests.get(f"{API_BASE_URL}/projects", timeout=10).json()


st.set_page_config(
    page_title="Freelance Project Finder",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Freelance Project Finder AI Agent")
st.caption("Find free-to-apply gigs, rank them, and explain why they match you.")

try:
    projects = load_projects()
except Exception as exc:
    st.error(f"Could not connect to API: {exc}")
    st.stop()

df = pd.DataFrame(projects)

if df.empty:
    st.warning("No projects found. Run collection first.")
    st.stop()

# Backward compatibility if old DB/API does not yet include these columns
for column, default in {
    "is_free_to_apply": "unknown",
    "apply_cost": "unknown",
    "opportunity_type": "unknown",
}.items():
    if column not in df.columns:
        df[column] = default

# Create readable badge-style columns for the dashboard table.
df["Score"] = df["score"].apply(score_badge)
df["Free"] = df["is_free_to_apply"].apply(free_to_apply_badge)

col1, col2, col3, col4 = st.columns(4)

total_projects = len(df)
high_match = len(df[df["score"] >= 80])
free_to_apply = len(df[df["is_free_to_apply"] == "yes"])
platforms = df["platform"].nunique()

col1.metric("Total Projects", total_projects)
col2.metric("High Match", high_match)
col3.metric("Free to Apply", free_to_apply)
col4.metric("Platforms", platforms)

st.divider()

collect_col, filter_col = st.columns([1, 3])
with collect_col:
    if st.button("Collect Latest Jobs", use_container_width=True):
        try:
            response = requests.post(f"{API_BASE_URL}/collect", timeout=20)
            response.raise_for_status()
            result = response.json()
            st.success(
                f"Collection completed: {result.get('inserted', result.get('collected', 'done'))}"
            )
            projects = load_projects()
            df = pd.DataFrame(projects)
        except Exception as exc:
            st.error(f"Collection failed: {exc}")

with filter_col:
    search = st.text_input("Search projects", placeholder="python, fastapi, ai, docker...")

show_only_free = st.checkbox("Show only free-to-apply gigs", value=True)
min_score = st.slider("Minimum score", 0, 100, 50)

filtered_df = df.copy()

if search:
    search_lower = search.lower()
    filtered_df = filtered_df[
        filtered_df["title"].fillna("").str.lower().str.contains(search_lower, na=False)
        | filtered_df["skills"].fillna("").str.lower().str.contains(search_lower, na=False)
        | filtered_df["platform"].fillna("").str.lower().str.contains(search_lower, na=False)
        | filtered_df["opportunity_type"].fillna("").str.lower().str.contains(search_lower, na=False)
    ]

if show_only_free:
    filtered_df = filtered_df[filtered_df["is_free_to_apply"] == "yes"]

filtered_df = filtered_df[filtered_df["score"] >= min_score]

# Use the helper-generated columns in the filtered view so the display stays consistent.
filtered_df["Score"] = filtered_df["score"].apply(score_badge)
filtered_df["Free"] = filtered_df["is_free_to_apply"].apply(free_to_apply_badge)

st.subheader("Recommended Free Gigs")

columns_to_show = [
    "Score",
    "title",
    "platform",
    "Free",
    "budget",
    "skills",
    "difficulty",
    "url",
]

st.dataframe(
    filtered_df[columns_to_show],
    width="stretch",
    hide_index=True,
)

st.subheader("Score Explanation")

if filtered_df.empty:
    st.info("No projects match your filters.")
else:
    project_ids = filtered_df["id"].tolist()
    selected_id = st.selectbox("Select project ID", project_ids)

    if st.button("Explain Score"):
        result = requests.get(f"{API_BASE_URL}/projects/{selected_id}/score", timeout=10).json()

        st.write(f"### {result['title']}")
        st.metric("Calculated Score", result["calculated_score"])

        for reason in result["reasons"]:
            st.write(f"- {reason}")

    st.subheader("Generate Proposal")

    if st.button("Generate Proposal"):
        result = requests.get(
            f"{API_BASE_URL}/projects/{selected_id}/proposal",
            timeout=10,
        ).json()

        st.write(f"### Proposal for: {result['title']}")
        st.text_area(
            "Copy this proposal",
            value=result["proposal"],
            height=300,
        )
