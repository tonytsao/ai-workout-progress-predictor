import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np


def evaluate_exercise_model(exercise_df: pd.DataFrame) -> dict:
    if len(exercise_df) < 6:
        return {
            "exercise": exercise_df["exercise"].iloc[0],
            "error": "Not enough data for evaluation"
        }

    X = exercise_df[["day_number"]]
    y = exercise_df["estimated_1rm"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, shuffle=False
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    return {
        "exercise": exercise_df["exercise"].iloc[0],
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2)
    }


def evaluate_all_exercises(df: pd.DataFrame):

    results = []

    for exercise in df["exercise"].unique():

        exercise_df = df[df["exercise"] == exercise].copy()
        exercise_df = exercise_df.sort_values(by="date")

        result = evaluate_exercise_model(exercise_df)
        results.append(result)

    return results