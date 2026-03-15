from src.load_data import load_workout_data, validate_workout_data, summarize_workout_data
from src.preprocess import preprocess_workout_data, split_by_exercise, print_preprocessed_summary
from src.feature_engineering import build_features, print_feature_summary
from src.predict import predict_all_exercises, print_prediction_results
from src.plateau_detection import detect_plateau_all_exercises, print_plateau_results
from src.report import merge_results, format_report, print_report, save_report
from src.visualize import plot_estimated_1rm_progress, plot_prediction_trend

def main():
    file_path = "data/raw/sample_workout.csv"

    # Step 1: Load and validate data
    df = load_workout_data(file_path)
    validate_workout_data(df)
    summarize_workout_data(df)

    print("\n" + "=" * 50 + "\n")

    # Step 2: Preprocess data
    df_clean = preprocess_workout_data(df)
    grouped_data = split_by_exercise(df_clean)
    print_preprocessed_summary(df_clean, grouped_data)

    print("\n" + "=" * 50 + "\n")

    # Step 3: Feature engineering
    df_features = build_features(df_clean)
    print_feature_summary(df_features)

    print("\n" + "=" * 50 + "\n")

    # Step 4: Prediction
    prediction_results = predict_all_exercises(df_features)
    print_prediction_results(prediction_results)

    print("\n" + "=" * 50 + "\n")

    # Step 5: Plateau detection
    plateau_results = detect_plateau_all_exercises(df_features)
    print_plateau_results(plateau_results)

    print("\n" + "=" * 50 + "\n")

    # Step 6: Final report
    merged_results = merge_results(prediction_results, plateau_results)
    report_text = format_report(merged_results)
    print_report(report_text)
    save_report(report_text)

    print("\n" + "=" * 50 + "\n")

    # Step 7: Visualization
    plot_estimated_1rm_progress(df_features)
    plot_prediction_trend(df_features, prediction_results)

    print("Saved figure to outputs/figures/estimated_1rm_progress.png")
    print("Saved prediction trend figures to outputs/figures/")


if __name__ == "__main__":
    main()