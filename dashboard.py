import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "https://YOUR_CLOUD_RUN_URL"


st.set_page_config(page_title="AI Workout Analytics Platform", layout="wide")

st.title("🏋️ AI Workout Analytics Platform")
st.write("Analyze workout logs and generate adaptive workout plans.")


# -----------------------------
# Section 1: Workout Analysis
# -----------------------------
st.header("1. Upload Workout CSV for Analysis")

uploaded_file = st.file_uploader("Upload workout CSV", type=["csv"])

analysis_result = None
plateau_summary = {}

if uploaded_file is not None:
    if st.button("Run Analysis"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}

        try:
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, timeout=60)
            response.raise_for_status()
            result = response.json()

            if result["success"]:
                analysis_result = result["data"]

                st.success(result["message"])

                st.subheader("Prediction Results")
                pred_df = pd.DataFrame(analysis_result["predictions"])
                st.dataframe(pred_df, use_container_width=True)

                st.subheader("Plateau Detection")
                plateau_df = pd.DataFrame(analysis_result["plateau_detection"])
                st.dataframe(plateau_df, use_container_width=True)

                plateau_summary = {
                    row["exercise"]: row["plateau_risk"]
                    for row in analysis_result["plateau_detection"]
                }

                st.session_state["plateau_summary"] = plateau_summary

            else:
                st.error(result["message"])

        except Exception as e:
            st.error(f"Analysis failed: {e}")


# -----------------------------
# Section 2: Workout Planner
# -----------------------------
st.header("2. Generate Adaptive Workout Plan")

col1, col2, col3 = st.columns(3)

with col1:
    goal = st.selectbox("Goal", ["strength", "hypertrophy", "general_fitness"])

with col2:
    days_per_week = st.slider("Days per week", min_value=2, max_value=6, value=4)

with col3:
    experience = st.selectbox("Experience", ["beginner", "intermediate", "advanced"])

use_analysis = st.checkbox("Use latest analysis result for adaptive planning", value=True)

if st.button("Generate Plan"):
    plateau_summary = st.session_state.get("plateau_summary", {}) if use_analysis else {}

    payload = {
        "goal": goal,
        "days_per_week": days_per_week,
        "experience": experience,
        "plateau_summary": plateau_summary
    }

    try:
        response = requests.post(f"{API_BASE_URL}/planner", json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        if result["success"]:
            plan_data = result["data"]

            st.success(result["message"])

            st.subheader("Workout Plan")
            for day in plan_data["plan"]:
                st.markdown(f"**Day {day['day']} — {day['focus']}**")
                st.write(", ".join(day["exercises"]))

            st.subheader("Recommendation")
            st.write(plan_data["recommendation"])

            st.subheader("Adaptive Notes")
            for note in plan_data["adaptive_notes"]:
                st.write(f"- {note}")

            if plan_data.get("plateau_summary"):
                st.subheader("Used Plateau Summary")
                st.json(plan_data["plateau_summary"])

        else:
            st.error(result["message"])

    except Exception as e:
        st.error(f"Planner failed: {e}")