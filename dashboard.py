
from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from src.screening import screen_resumes


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Resume Screening | Recruiter Portal",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
JOB_FILE = BASE_DIR / "data" / "job_description.txt"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ==================================================
# SESSION STATE
# ==================================================

if "results" not in st.session_state:
    st.session_state.results = None

if "job_description" not in st.session_state:
    st.session_state.job_description = ""


# ==================================================
# ADVANCED DARK BLUE THEME
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1220;
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background-color: #111C33;
    border-right: 1px solid #1E3A8A;
}

[data-testid="stHeader"] {
    background-color: #0B1220;
}

h1, h2, h3, h4, p, label {
    color: #F8FAFC !important;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #60A5FA;
}

.subtitle {
    color: #94A3B8;
    font-size: 14px;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #172554,
        #14213D
    );
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #2563EB;
}

[data-testid="stMetricValue"] {
    color: #60A5FA !important;
}

[data-testid="stMetricLabel"] {
    color: #BFDBFE !important;
}

.stButton > button {
    background: linear-gradient(
        90deg,
        #2563EB,
        #1D4ED8
    );
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
    min-height: 42px;
}

.stButton > button:hover {
    background: #1E40AF;
    color: white;
}

div[data-testid="stFileUploader"] {
    background: #111C33;
    border: 1px dashed #3B82F6;
    border-radius: 12px;
    padding: 15px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #1E40AF;
    border-radius: 10px;
}

section[data-testid="stVerticalBlock"] {
    gap: 1rem;
}

hr {
    border-color: #1E3A8A;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Screening</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent Recruitment Analytics & Candidate Management Portal'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("⚙️ Recruiter Settings")

st.sidebar.markdown("### Screening Configuration")

threshold = st.sidebar.slider(
    "Minimum review score",
    min_value=0,
    max_value=100,
    value=50
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Supported Formats")

st.sidebar.write("📄 PDF")
st.sidebar.write("📝 DOCX")
st.sidebar.write("📃 TXT")

st.sidebar.markdown("---")

if st.sidebar.button("🗑️ Clear Screening Results"):
    st.session_state.results = None
    st.rerun()

st.sidebar.caption(
    "AI Resume Screening Tool | Version 2.0"
)


# ==================================================
# LOAD JOB DESCRIPTION
# ==================================================

if not JOB_FILE.exists():
    st.error("Job description file is missing.")
    st.stop()

if not st.session_state.job_description:
    st.session_state.job_description = JOB_FILE.read_text(
        encoding="utf-8"
    )


# ==================================================
# MAIN TABS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "👥 Candidates",
    "🧠 Skill Insights",
    "📁 Reports & Settings"
])


# ==================================================
# TAB 1 - OVERVIEW
# ==================================================

with tab1:

    st.subheader("Recruitment Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Screening Engine",
            "TF-IDF + NLP"
        )

    with col2:
        st.metric(
            "Scoring Model",
            "60% + 40%"
        )

    st.markdown("### Job Description")

    with st.expander("View or edit job description", expanded=False):

        edited_job = st.text_area(
            "Job requirements",
            value=st.session_state.job_description,
            height=220
        )

        if st.button("Save Job Description"):

            if edited_job.strip():
                st.session_state.job_description = edited_job
                st.success("Job description updated.")
            else:
                st.warning("Job description cannot be empty.")

    st.markdown("### Upload Resumes")

    uploaded_files = st.file_uploader(
        "Upload multiple candidate resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="resume_upload"
    )

    st.caption(
        "You can upload multiple PDF, DOCX or TXT resumes."
    )

    if uploaded_files:

        st.info(
            f"{len(uploaded_files)} resume(s) selected."
        )

    if st.button(
        "🚀 Analyze & Rank Candidates",
        use_container_width=True
    ):

        if not uploaded_files:

            st.warning("Please upload at least one resume.")

        elif not st.session_state.job_description.strip():

            st.error("Please enter a job description.")

        else:

            try:

                with tempfile.TemporaryDirectory() as temp_dir:

                    temp_dir = Path(temp_dir)
                    resume_paths = []

                    for uploaded_file in uploaded_files:

                        file_path = temp_dir / uploaded_file.name

                        file_path.write_bytes(
                            uploaded_file.getbuffer()
                        )

                        resume_paths.append(file_path)

                    with st.spinner(
                        "AI engine is analyzing candidate resumes..."
                    ):

                        results = screen_resumes(
                            resume_paths,
                            st.session_state.job_description,
                            threshold=threshold
                        )

                    st.session_state.results = results

                st.success(
                    "Candidate analysis completed successfully!"
                )

            except Exception as error:

                st.error(f"Screening error: {error}")


    # ----------------------------------------------
    # DASHBOARD METRICS
    # ----------------------------------------------

    if st.session_state.results is not None:

        df = pd.DataFrame(st.session_state.results)

        st.divider()
        st.subheader("Live Screening Statistics")

        total = len(df)

        shortlisted = len(
            df[df["status"] == "Shortlisted for Review"]
        )

        needs_review = total - shortlisted

        average_score = round(
            df["final_score"].mean(),
            2
        ) if total else 0

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Candidates", total)
        c2.metric("Shortlisted for Review", shortlisted)
        c3.metric("Needs Manual Review", needs_review)
        c4.metric("Average Match Score", f"{average_score}%")

        st.markdown("### Candidate Score Distribution")

        score_chart = df.set_index("candidate")[
            ["final_score"]
        ]

        st.bar_chart(
            score_chart,
            use_container_width=True
        )


# ==================================================
# TAB 2 - CANDIDATES
# ==================================================

with tab2:

    st.subheader("Candidate Management")

    if st.session_state.results is None:

        st.info("Upload resumes and run screening first.")

    else:

        df = pd.DataFrame(st.session_state.results)

        search = st.text_input(
            "🔍 Search candidate",
            placeholder="Enter candidate name..."
        )

        status_options = [
            "All",
            "Shortlisted for Review",
            "Needs Manual Review"
        ]

        selected_status = st.selectbox(
            "Filter by review status",
            status_options
        )

        minimum_score = st.slider(
            "Minimum candidate score",
            0,
            100,
            0,
            key="candidate_min_score"
        )

        filtered_df = df.copy()

        if search:

            filtered_df = filtered_df[
                filtered_df["candidate"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if selected_status != "All":

            filtered_df = filtered_df[
                filtered_df["status"] == selected_status
            ]

        filtered_df = filtered_df[
            filtered_df["final_score"] >= minimum_score
        ]

        st.write(
            f"Showing {len(filtered_df)} candidate(s)"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Candidate Profile Details")

        if not filtered_df.empty:

            candidate_names = filtered_df["candidate"].tolist()

            selected_candidate = st.selectbox(
                "Select candidate",
                candidate_names
            )

            candidate = filtered_df[
                filtered_df["candidate"] == selected_candidate
            ].iloc[0]

            a, b, c = st.columns(3)

            a.metric(
                "Final Score",
                f"{candidate['final_score']}%"
            )

            b.metric(
                "Similarity",
                f"{candidate['similarity_score']}%"
            )

            c.metric(
                "Skill Match",
                f"{candidate['skill_match']}%"
            )

            st.write("**Matched Skills**")

            st.success(
                candidate["matched_skills"] or "No matched skills"
            )

            st.write("**Missing Skills**")

            st.warning(
                candidate["missing_skills"] or "No missing skills"
            )

            st.write("**Review Status**")

            st.info(candidate["status"])


# ==================================================
# TAB 3 - SKILL INSIGHTS
# ==================================================

with tab3:

    st.subheader("Technical Skill Analytics")

    if st.session_state.results is None:

        st.info("Run screening to see skill analytics.")

    else:

        df = pd.DataFrame(st.session_state.results)

        skill_counts = {}

        for skills in df["matched_skills"].fillna(""):

            for skill in skills.split(","):

                skill = skill.strip()

                if skill:

                    skill_counts[skill] = (
                        skill_counts.get(skill, 0) + 1
                    )

        if skill_counts:

            skill_df = pd.DataFrame(
                list(skill_counts.items()),
                columns=["Skill", "Candidate Count"]
            )

            skill_df = skill_df.sort_values(
                "Candidate Count",
                ascending=False
            )

            st.markdown("### Most Common Matched Skills")

            st.bar_chart(
                skill_df.set_index("Skill"),
                use_container_width=True
            )

            st.dataframe(
                skill_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("No matched skills were found.")


# ==================================================
# TAB 4 - REPORTS AND SETTINGS
# ==================================================

with tab4:

    st.subheader("Reports & Export Center")

    if st.session_state.results is None:

        st.info("No screening report available yet.")

    else:

        df = pd.DataFrame(st.session_state.results)

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.markdown("### Download Screening Report")

        st.download_button(
            label="⬇️ Download CSV Report",
            data=csv_data,
            file_name="resume_screening_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("### Screening Information")

        st.write(
            f"Total processed resumes: {len(df)}"
        )

        st.write(
            "Scoring formula: 60% TF-IDF similarity + 40% skill match."
        )

        st.write(
            f"Review threshold: {threshold}%"
        )

        st.caption(
            "The score is a screening aid, not a probability of "
            "job performance or an automatic hiring decision."
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    "<center style='color:#64748B;'>"
    "Automated Resume Screening Tool | "
    "Python • NLP • TF-IDF • FastAPI • Streamlit"
    "</center>",
    unsafe_allow_html=True
)
