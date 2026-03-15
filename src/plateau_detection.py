import pandas as pd


def detect_plateau_for_exercise(exercise_df: pd.DataFrame) -> dict:
    """
    Detect plateau risk for a single exercise based on the last 4 sessions.
    """
    exercise_df = exercise_df.sort_values(by="date").reset_index(drop=True)

    if len(exercise_df) < 4:
        return {
            "exercise": exercise_df["exercise"].iloc[0],
            "plateau_risk": "Not enough data",
            "reason": "Need at least 4 sessions to detect plateau."
        }

    recent_df = exercise_df.tail(4).copy()

    first_1rm = recent_df["estimated_1rm"].iloc[0]
    last_1rm = recent_df["estimated_1rm"].iloc[-1]
    progress_rate = (last_1rm - first_1rm) / first_1rm

    first_volume = recent_df["volume"].iloc[0]
    last_volume = recent_df["volume"].iloc[-1]
    volume_change = (last_volume - first_volume) / first_volume

    if progress_rate >= 0.01:
        plateau_risk = "Low"
        reason = "Estimated 1RM has improved over the last 4 sessions."
    elif progress_rate < 0.01 and volume_change <= 0:
        plateau_risk = "Medium"
        reason = "Estimated 1RM has changed very little over the last 4 sessions."
    else:
        plateau_risk = "High"
        reason = "Estimated 1RM has changed very little while training volume increased."

    return {
        "exercise": exercise_df["exercise"].iloc[0],
        "plateau_risk": plateau_risk,
        "reason": reason,
        "progress_rate": round(progress_rate * 100, 2),
        "volume_change_rate": round(volume_change * 100, 2),
    }


def detect_plateau_all_exercises(df: pd.DataFrame) -> list[dict]:
    """
    Detect plateau risk for all exercises.
    """
    results = []

    for exercise in df["exercise"].unique():
        exercise_df = df[df["exercise"] == exercise].copy()
        result = detect_plateau_for_exercise(exercise_df)
        results.append(result)

    return results


def print_plateau_results(results: list[dict]) -> None:
    """
    Print plateau detection results in a readable format.
    """
    print("Plateau detection complete.\n")

    for result in results:
        print(f"Exercise: {result['exercise']}")
        print(f"Plateau risk: {result['plateau_risk']}")
        print(f"Reason: {result['reason']}")

        if "progress_rate" in result:
            print(f"1RM change (last 4 sessions): {result['progress_rate']}%")
            print(f"Volume change (last 4 sessions): {result['volume_change_rate']}%")

        print("-" * 40)

def add_training_score(plateau_results: list[dict]) -> list[dict]:
    """
    Add a simple training score and status based on plateau risk.
    """
    score_map = {
        "Low": 85,
        "Medium": 65,
        "High": 40,
        "Not enough data": 50,
    }

    for result in plateau_results:
        score = score_map.get(result["plateau_risk"], 50)

        if score >= 80:
            status = "On Track"
        elif score >= 60:
            status = "Watch Progress"
        else:
            status = "Needs Adjustment"

        result["training_score"] = score
        result["training_status"] = status

    return plateau_results