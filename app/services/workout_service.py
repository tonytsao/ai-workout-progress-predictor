from src.load_data import validate_workout_data
from src.preprocess import preprocess_workout_data
from src.feature_engineering import build_features
from src.predict import predict_all_exercises, make_prediction_results_json_safe
from src.plateau_detection import detect_plateau_all_exercises, add_training_score


def analyze_workout_dataframe(df):
    validate_workout_data(df)
    df_clean = preprocess_workout_data(df)
    df_features = build_features(df_clean)

    prediction_results = predict_all_exercises(df_features)
    plateau_results = detect_plateau_all_exercises(df_features)
    plateau_results = add_training_score(plateau_results)

    return {
        "predictions": make_prediction_results_json_safe(prediction_results),
        "plateau_detection": plateau_results,
    }