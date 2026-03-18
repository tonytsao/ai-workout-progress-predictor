import streamlit as st
import pandas as pd

from src.load_data import validate_workout_data
from src.preprocess import preprocess_workout_data
from src.feature_engineering import build_features
from src.predict import predict_all_exercises, make_prediction_results_json_safe
from src.plateau_detection import detect_plateau_all_exercises, add_training_score


st.title("🏋️ AI Workout Progress Analyzer")

st.write("Upload your workout CSV file to analyze training progress.")


uploaded_file = st.file_uploader("Upload workout CSV", type=["csv"])


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    try:

        validate_workout_data(df)
        df_clean = preprocess_workout_data(df)
        df_features = build_features(df_clean)

        predictions = predict_all_exercises(df_features)
        plateau = detect_plateau_all_exercises(df_features)
        plateau = add_training_score(plateau)

        predictions = make_prediction_results_json_safe(predictions)

        st.subheader("Prediction Results")

        pred_df = pd.DataFrame(predictions)
        st.dataframe(pred_df)

        st.subheader("Plateau Detection")

        plateau_df = pd.DataFrame(plateau)
        st.dataframe(plateau_df)

        st.subheader("Estimated 1RM Progress")

        for exercise in df_features["exercise"].unique():

            exercise_df = df_features[df_features["exercise"] == exercise]

            st.line_chart(
                exercise_df.set_index("date")["estimated_1rm"]
            )

    except Exception as e:

        st.error(str(e))