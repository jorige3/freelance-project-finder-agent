import os
import pandas as pd
import requests
import streamlit as st

from dashboard.helpers import score_badge, is_free_to_apply, free_to_apply_badge

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8010")


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
    "difficulty": "unknown",
    "budget": None,
    "skills": None,
    "url": None,
}.items():
    if column not in df.columns:
        df[column] = default

# Ensure score is numeric so comparisons don't blow up on messy data
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# Create readable badge-style columns for the dashboard table.
df["Score"] = df["score"].apply(score_badge)
df["Free"] = df["is_free_to_apply"].apply(free_to_apply_badge)

col1, col2, col3, col4 = st.columns(4)

total_projects = len(df)
high_match = int((df["score"] >= 80).sum())
free_to_apply_count = int(df["is_free_to_apply"].apply(is_free_to_apply).sum())
platforms = df["platform"].nunique()

col1.metric("Total Projects", total_projects)
col2.metric("High Match", high_match)
col3.metric("Free to Apply", free_to_apply_count)
col4.metric("Platforms", platforms)

st.divider()

st.subheader("🏆 Today's Top 5 AI Picks")

try:
    top_picks_response = requests.get(
        f"{API_BASE_URL}/agents/top-free-gigs",
        timeout=10,
    )
    top_picks_response.raise_for_status()
    top_picks = top_picks_response.json().get("projects", [])
except Exception as exc:
    st.warning(f"Could not load AI picks: {exc}")
    top_picks = []

if top_picks:
    medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]
    for index, project in enumerate(top_picks[:5], start=1):
        medal = medals[index - 1]

        with st.container(border=True):
            st.markdown(f"### {medal} {project.get('title', 'Untitled')}")
            st.write(f"**Platform:** {project.get('platform', 'Unknown')}")
            st.write(f"**Score:** {score_badge(project.get('score'))}")
            st.write(f"**Budget:** {project.get('budget') or 'Not listed'}")
            st.write(f"**Skills:** {project.get('skills') or 'Not listed'}")
            st.write("🆓 **Free to apply**")

            reasons = (project.get("explanation") or {}).get("reasons", [])
            if reasons:
                with st.expander("Why this is recommended"):
                    for reason in reasons:
                        st.write(f"- {reason}")

            with st.expander("Generated Proposal"):
                st.text_area(
                    "Proposal",
                    value=project.get("proposal", ""),
                    height=220,
                    key=f"proposal_{project.get('id')}",
                )
else:
    st.info("No AI picks available yet. Try collecting projects first.")

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
            df["score"] = pd.to_numeric(df.get("score"), errors="coerce")
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
        | filtered_df["skills"].fillna("").astype(str).str.lower().str.contains(search_lower, na=False)
        | filtered_df["platform"].fillna("").str.lower().str.contains(search_lower, na=False)
        | filtered_df["opportunity_type"].fillna("").astype(str).str.lower().str.contains(search_lower, na=False)
    ]

if show_only_free:
    filtered_df = filtered_df[filtered_df["is_free_to_apply"].apply(is_free_to_apply)]

filtered_df = filtered_df[filtered_df["score"].fillna(-1) >= min_score]

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

# Guard against any columns still missing at display time
for column in columns_to_show:
    if column not in filtered_df.columns:
        filtered_df[column] = None

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
        try:
            result = requests.get(
                f"{API_BASE_URL}/projects/{selected_id}/score", timeout=10
            ).json()

            st.write(f"### {result.get('title', 'Untitled')}")
            st.metric("Calculated Score", result.get("calculated_score", "N/A"))

            for reason in result.get("reasons", []):
                st.write(f"- {reason}")
        except Exception as exc:
            st.error(f"Could not fetch score explanation: {exc}")

    st.subheader("Generate Proposal")

    if st.button("Generate Proposal"):
        try:
            result = requests.get(
                f"{API_BASE_URL}/projects/{selected_id}/proposal",
                timeout=10,
            ).json()

            st.write(f"### Proposal for: {result.get('title', 'Untitled')}")
            st.text_area(
                "Copy this proposal",
                value=result.get("proposal", ""),
                height=300,
            )
        except Exception as exc:
            st.error(f"Could not generate proposal: {exc}")

    st.subheader("📌 Application Tracker")

    status_options = [
        "saved",
        "proposal_ready",
        "applied",
        "interview",
        "offer",
        "completed",
        "rejected",
    ]

    tracker_project_id = st.selectbox(
        "Select project to track",
        filtered_df["id"].tolist(),
        key="tracker_project_id",
    )

    try:
        current_application = requests.get(
            f"{API_BASE_URL}/projects/{tracker_project_id}/application",
            timeout=10,
        ).json()
    except Exception as exc:
        st.error(f"Could not load application status: {exc}")
        current_application = {}

    current_status = current_application.get("application_status", "saved")

    status_index = (
        status_options.index(current_status)
        if current_status in status_options
        else 0
    )

    selected_status = st.selectbox(
        "Application status",
        status_options,
        index=status_index,
    )

    application_notes = st.text_area(
        "Notes",
        value=current_application.get("notes") or "",
        placeholder="Example: Proposal sent. Waiting for client response.",
        height=120,
    )

    if st.button("💾 Save Application Status"):
        try:
            response = requests.patch(
                f"{API_BASE_URL}/projects/{tracker_project_id}/application",
                json={
                    "status": selected_status,
                    "notes": application_notes,
                },
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()

            st.success("Application status updated successfully.")
            st.write(f"**Project:** {result.get('title', 'Untitled')}")
            st.write(f"**Status:** {result.get('application_status', selected_status)}")

            if result.get("applied_at"):
                st.write(f"**Applied at:** {result['applied_at']}")

            if result.get("notes"):
                st.write(f"**Notes:** {result['notes']}")

        except Exception as exc:
            st.error(f"Could not update application status: {exc}")