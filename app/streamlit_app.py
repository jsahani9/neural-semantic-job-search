"""
Streamlit UI for Neural Semantic Job Search
- Upload resume PDF
- Call FastAPI /match
- Display ranked job matches
"""

from __future__ import annotations

import os
import requests
import streamlit as st


# -----------------------
# Config
# -----------------------
st.set_page_config(page_title="Neural Semantic Job Search", layout="wide")
st.title("🧠 Neural Semantic Job Search")
st.caption("Upload your resume → get ranked job matches (FastAPI + Adzuna + AWS Bedrock).")

API_BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")



# -----------------------
# Sidebar controls
# -----------------------
st.sidebar.header("Search Settings")

keywords = st.sidebar.text_input("Keywords", value="software engineer")
location = st.sidebar.text_input("Location", value="Canada")

max_results = st.sidebar.number_input("Adzuna max_results", min_value=5, max_value=50, value=20, step=5)
top_n = st.sidebar.number_input("Top N results", min_value=1, max_value=20, value=10, step=1)

# limit = how many jobs you actually score with LLM (cost control)
limit = st.sidebar.number_input("LLM scoring limit (cost control)", min_value=1, max_value=25, value=8, step=1)

st.sidebar.markdown("---")
st.sidebar.write("API Base URL:")
st.sidebar.code(API_BASE_URL)


# -----------------------
# Health check
# -----------------------
with st.expander("✅ Backend status"):
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=5)
        st.write("Status code:", r.status_code)
        st.json(r.json())
    except Exception as e:
        st.error(f"Could not reach backend at {API_BASE_URL}. Error: {e}")
        st.stop()


# -----------------------
# Upload + Match
# -----------------------
uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

col1, col2 = st.columns([1, 1])

with col1:
    run_btn = st.button("🔎 Find Matching Jobs", type="primary", disabled=(uploaded is None))

with col2:
    st.write("")
    st.write("Tip: Start with **limit=5** for faster + cheaper runs.")


if run_btn:
    if uploaded is None:
        st.warning("Please upload a PDF first.")
        st.stop()

    with st.spinner("Uploading resume + matching jobs..."):
        try:
            files = {
                "resume": (uploaded.name, uploaded.getvalue(), "application/pdf")
            }

            params = {
                "keywords": keywords,
                "location": location,
                "max_results": int(max_results),
                "top_n": int(top_n),
                "limit": int(limit),
            }

            resp = requests.post(f"{API_BASE_URL}/match", params=params, files=files, timeout=300)
            resp.raise_for_status()
            data = resp.json()

        except requests.HTTPError as e:
            st.error("Backend returned an error.")
            st.code(resp.text if "resp" in locals() else str(e))
            st.stop()

        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

    # -----------------------
    # Results
    # -----------------------
    st.success("✅ Done!")

    st.subheader("🧾 Profile Preview")
    st.code(data.get("profile_preview", "")[:1200])

    st.subheader("💼 Top Matches")
    matches = data.get("matches", [])

    if not matches:
        st.warning("No matches returned.")
        st.stop()

    # Sort display (just in case)
    matches = sorted(matches, key=lambda x: x.get("match_score", 0), reverse=True)

    for i, job in enumerate(matches, 1):
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        loc = job.get("location", "N/A")
        score = job.get("match_score", 0)
        url = job.get("url", "")
        reason = job.get("match_reason", "")

        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"### {i}. {title}")
                st.write(f"**Company:** {company}")
                st.write(f"**Location:** {loc}")
                if url:
                    st.markdown(f"🔗 **Link:** {url}")
            with c2:
                st.metric("Score", f"{score}/100")

            st.write("**Reason:**")
            st.write(reason)

            # Optional: show a short description preview (if present)
            desc = job.get("description", "")
            if desc:
                with st.expander("Job description (preview)"):
                    st.write(desc[:800] + ("..." if len(desc) > 800 else ""))
