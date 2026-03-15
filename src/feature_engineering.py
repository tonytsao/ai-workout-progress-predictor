import pandas as pd


def add_estimated_1rm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add estimated 1RM using the Epley formula:
    1RM = weight * (1 + reps / 30)
    """
    df = df.copy()
    df["estimated_1rm"] = df["weight"] * (1 + df["reps"] / 30)
    return df


def add_volume(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add training volume = weight * reps * sets
    """
    df = df.copy()
    df["volume"] = df["weight"] * df["reps"] * df["sets"]
    return df


def add_day_number(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add day_number based on the number of days since the first workout date.
    """
    df = df.copy()
    first_date = df["date"].min()
    df["day_number"] = (df["date"] - first_date).dt.days
    return df


def add_session_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add session index for each exercise separately.
    """
    df = df.copy()
    df["session_index"] = df.groupby("exercise").cumcount() + 1
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run all feature engineering steps.
    """
    df = add_estimated_1rm(df)
    df = add_volume(df)
    df = add_day_number(df)
    df = add_session_index(df)
    return df


def print_feature_summary(df: pd.DataFrame) -> None:
    """
    Print a preview of the engineered features.
    """
    print("Feature engineering complete.\n")
    print(df.head(10)[
        ["date", "exercise", "weight", "reps", "sets", "estimated_1rm", "volume", "day_number", "session_index"]
    ])