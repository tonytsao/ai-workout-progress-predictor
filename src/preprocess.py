import pandas as pd


def preprocess_workout_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize workout data for later analysis.
    """
    df = df.copy()

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    # Standardize exercise names
    df["exercise"] = df["exercise"].str.strip().str.lower()

    # Sort by date
    df = df.sort_values(by="date").reset_index(drop=True)

    return df


def split_by_exercise(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Split workout data into separate dataframes by exercise.
    """
    exercise_groups = {}

    for exercise in df["exercise"].unique():
        exercise_df = df[df["exercise"] == exercise].copy()
        exercise_df = exercise_df.reset_index(drop=True)
        exercise_groups[exercise] = exercise_df

    return exercise_groups


def print_preprocessed_summary(df: pd.DataFrame, grouped_data: dict[str, pd.DataFrame]) -> None:
    """
    Print summary after preprocessing.
    """
    print("Preprocessing complete.\n")
    print("Sorted data preview:")
    print(df.head(), "\n")

    print("Grouped by exercise:")
    for exercise, exercise_df in grouped_data.items():
        print(f"- {exercise}: {len(exercise_df)} rows")