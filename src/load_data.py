from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = ["date", "exercise", "weight", "reps", "sets", "rpe"]
VALID_EXERCISES = {"bench_press", "squat", "deadlift"}


def load_workout_data(file_path: str) -> pd.DataFrame:
    """
    Load workout data from a CSV file and perform basic validation.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(path)

    # Check required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Check empty dataframe
    if df.empty:
        raise ValueError("The input CSV is empty.")

    return df


def validate_workout_data(df: pd.DataFrame) -> None:
    """
    Validate basic data format and values.
    """
    # Check missing values in required columns
    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Some required fields contain missing values.")

    # Validate exercise names
    invalid_exercises = set(df["exercise"]) - VALID_EXERCISES
    if invalid_exercises:
        raise ValueError(f"Invalid exercise names found: {invalid_exercises}")

    # Validate numeric columns
    numeric_columns = ["weight", "reps", "sets", "rpe"]
    for col in numeric_columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric.")

    # Validate positive numbers
    for col in ["weight", "reps", "sets"]:
        if (df[col] <= 0).any():
            raise ValueError(f"Column '{col}' must contain positive values.")

    # Validate date format
    try:
        pd.to_datetime(df["date"], format="%Y-%m-%d")
    except ValueError as e:
        raise ValueError("Column 'date' must use YYYY-MM-DD format.") from e


def summarize_workout_data(df: pd.DataFrame) -> None:
    """
    Print a simple summary of the loaded workout data.
    """
    print(f"Loaded {len(df)} workout records.\n")

    print("Exercises found:")
    for exercise, count in df["exercise"].value_counts().items():
        print(f"- {exercise}: {count} records")

    print("\nDate range:")
    print(f"- Start: {df['date'].min()}")
    print(f"- End:   {df['date'].max()}")


if __name__ == "__main__":
    file_path = "data/raw/sample_workout.csv"

    df = load_workout_data(file_path)
    validate_workout_data(df)
    summarize_workout_data(df)