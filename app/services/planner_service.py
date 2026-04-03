from src.planner import generate_workout_plan


def create_workout_plan(goal: str, days_per_week: int, experience: str) -> dict:
    return generate_workout_plan(
        goal=goal,
        days_per_week=days_per_week,
        experience=experience,
    )