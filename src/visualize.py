from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_estimated_1rm_progress(
    df: pd.DataFrame,
    output_path: str = "outputs/figures/estimated_1rm_progress.png"
) -> None:
    """
    Plot estimated 1RM progress for each exercise and save as a PNG file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    for exercise in df["exercise"].unique():
        exercise_df = df[df["exercise"] == exercise].copy()
        exercise_df = exercise_df.sort_values(by="date")

        plt.plot(
            exercise_df["date"],
            exercise_df["estimated_1rm"],
            marker="o",
            label=exercise
        )

    plt.xlabel("Date")
    plt.ylabel("Estimated 1RM (kg)")
    plt.title("Estimated 1RM Progress by Exercise")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_prediction_trend(
    df: pd.DataFrame,
    prediction_results: list[dict],
    output_dir: str = "outputs/figures"
) -> None:
    """
    Plot historical estimated 1RM and future prediction points for each exercise.
    Save one figure per exercise.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for result in prediction_results:
        exercise = result["exercise"]
        model = result["model"]

        exercise_df = df[df["exercise"] == exercise].copy()
        exercise_df = exercise_df.sort_values(by="day_number")

        # Historical data
        x_hist = exercise_df["day_number"]
        y_hist = exercise_df["estimated_1rm"]

        # Trend line range
        x_min = x_hist.min()
        x_max = result["pred_day_8_weeks"]
        x_line = pd.DataFrame({"day_number": range(x_min, x_max + 1)})
        y_line = model.predict(x_line)

        # Future prediction points
        x_future = [result["pred_day_4_weeks"], result["pred_day_8_weeks"]]
        y_future = [result["predicted_4_week_1rm"], result["predicted_8_week_1rm"]]

        plt.figure(figsize=(8, 5))
        plt.plot(x_hist, y_hist, marker="o", label="historical 1RM")
        plt.plot(x_line["day_number"], y_line, linestyle="--", label="trend line")
        plt.scatter(x_future, y_future, marker="x", s=100, label="future prediction")

        plt.xlabel("Day Number")
        plt.ylabel("Estimated 1RM (kg)")
        plt.title(f"Prediction Trend - {exercise}")
        plt.legend()
        plt.tight_layout()

        file_name = f"{exercise}_prediction_trend.png"
        plt.savefig(output_path / file_name)
        plt.close()