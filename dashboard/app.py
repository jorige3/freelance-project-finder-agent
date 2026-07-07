import pandas as pd
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8010"

st.set_page_config(
    page_title="Freelance Project Finder",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Freelance Project Finder AI Agent")
st.caption("Find free-to-apply gigs, rank them, and explain why they match you.")

try:
    projects = requests.get(f"{API_BASE_URL}/projects", timeout=10).json()
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

search = st.text_input("Search projects", placeholder="python, fastapi, ai, docker...")

show_only_free = st.checkbox("Show only free-to-apply gigs", value=True)

min_score = st.slider("Minimum score", 0, 100, 50)

filtered_df = df.copy()

if search:
    search_lower = search.lower()
    filtered_df = filtered_df[
        filtered_df["title"].str.lower().str.contains(search_lower, na=False)
        | filtered_df["skills"].str.lower().str.contains(search_lower, na=False)
        | filtered_df["platform"].str.lower().str.contains(search_lower, na=False)
        | filtered_df["opportunity_type"].str.lower().str.contains(search_lower, na=False)
    ]

if show_only_free:
    filtered_df = filtered_df[filtered_df["is_free_to_apply"] == "yes"]

filtered_df = filtered_df[filtered_df["score"] >= min_score]

st.subheader("Recommended Free Gigs")

columns_to_show = [
    "score",
    "title",
    "platform",
    "budget",
    "skills",
    "difficulty",
    "is_free_to_apply",
    "apply_cost",
    "opportunity_type",
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
    st.stop()

project_ids = filtered_df["id"].tolist()
selected_id = st.selectbox("Select project ID", project_ids)

if st.button("Explain Score"):
    result = requests.get(f"{API_BASE_URL}/projects/{selected_id}/score", timeout=10).json()

    st.write(f"### {result['title']}")
    st.metric("Calculated Score", result["calculated_score"])

    for reason in result["reasons"]:
        st.write(f"- {reason}")
