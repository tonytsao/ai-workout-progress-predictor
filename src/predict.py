import pandas as pd
from sklearn.linear_model import LinearRegression


def train_and_predict_for_exercise(exercise_df: pd.DataFrame) -> dict:
    """
    Train a simple linear regression model for one exercise and predict
    estimated 1RM for 4 weeks and 8 weeks into the future.
    """
    if len(exercise_df) < 2:
        raise ValueError("Not enough data points to train prediction model.")

    X = exercise_df[["day_number"]]
    y = exercise_df["estimated_1rm"]

    model = LinearRegression()
    model.fit(X, y)

    latest_row = exercise_df.iloc[-1]
    latest_day = latest_row["day_number"]
    current_1rm = latest_row["estimated_1rm"]

    day_4_weeks = latest_day + 28
    day_8_weeks = latest_day + 56

    pred_4_weeks = model.predict([[day_4_weeks]])[0]
    pred_8_weeks = model.predict([[day_8_weeks]])[0]

    return {
        "exercise": latest_row["exercise"],
        "current_estimated_1rm": round(current_1rm, 2),
        "predicted_4_week_1rm": round(pred_4_weeks, 2),
        "predicted_8_week_1rm": round(pred_8_weeks, 2),
        "latest_day_number": int(latest_day),
        "pred_day_4_weeks": int(day_4_weeks),
        "pred_day_8_weeks": int(day_8_weeks),
        "model": model,
    }


def predict_all_exercises(df: pd.DataFrame) -> list[dict]:
    """
    Train separate models for each exercise and return prediction results.
    """
    results = []

    for exercise in df["exercise"].unique():
        exercise_df = df[df["exercise"] == exercise].copy()
        exercise_df = exercise_df.sort_values(by="date").reset_index(drop=True)

        result = train_and_predict_for_exercise(exercise_df)
        results.append(result)

    return results


def print_prediction_results(results: list[dict]) -> None:
    """
    Print prediction results in a readable format.
    """
    print("Prediction complete.\n")

    for result in results:
        print(f"Exercise: {result['exercise']}")
        print(f"Current estimated 1RM: {result['current_estimated_1rm']} kg")
        print(f"Predicted 4-week 1RM: {result['predicted_4_week_1rm']} kg")
        print(f"Predicted 8-week 1RM: {result['predicted_8_week_1rm']} kg")
        print("-" * 40)