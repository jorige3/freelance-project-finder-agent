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
st.caption("Find, rank, and explain freelance opportunities.")

col1, col2, col3 = st.columns(3)

try:
    projects = requests.get(f"{API_BASE_URL}/projects", timeout=10).json()
except Exception as exc:
    st.error(f"Could not connect to API: {exc}")
    st.stop()

df = pd.DataFrame(projects)

if df.empty:
    st.warning("No projects found. Run collection first.")
    st.stop()

total_projects = len(df)
high_match = len(df[df["score"] >= 80])
platforms = df["platform"].nunique()

col1.metric("Total Projects", total_projects)
col2.metric("High Match", high_match)
col3.metric("Platforms", platforms)

search = st.text_input("Search projects", placeholder="python, fastapi, ai, docker...")

if search:
    search_lower = search.lower()
    df = df[
        df["title"].str.lower().str.contains(search_lower, na=False)
        | df["skills"].str.lower().str.contains(search_lower, na=False)
        | df["platform"].str.lower().str.contains(search_lower, na=False)
    ]

min_score = st.slider("Minimum score", 0, 100, 50)
df = df[df["score"] >= min_score]

st.subheader("Recommended Projects")

st.dataframe(
    df[["score", "title", "platform", "budget", "skills", "difficulty", "url"]],
    width="stretch",
    hide_index=True,
)

st.subheader("Score Explanation")

project_ids = df["id"].tolist()
selected_id = st.selectbox("Select project ID", project_ids)

if st.button("Explain Score"):
    result = requests.get(f"{API_BASE_URL}/projects/{selected_id}/score", timeout=10).json()

    st.write(f"### {result['title']}")
    st.metric("Calculated Score", result["calculated_score"])

    for reason in result["reasons"]:
        st.write(f"- {reason}")
