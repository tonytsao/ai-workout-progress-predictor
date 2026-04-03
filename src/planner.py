def generate_workout_plan(goal: str, days_per_week: int, experience: str, plateau_summary: dict | None = None) -> dict:
    """
    Generate a simple rule-based workout plan, optionally adjusted by plateau status.
    """
    goal = goal.lower()
    experience = experience.lower()
    plateau_summary = plateau_summary or {}

    if goal not in {"strength", "hypertrophy", "general_fitness"}:
        raise ValueError("goal must be one of: strength, hypertrophy, general_fitness")

    if experience not in {"beginner", "intermediate", "advanced"}:
        raise ValueError("experience must be one of: beginner, intermediate, advanced")

    if not (2 <= days_per_week <= 6):
        raise ValueError("days_per_week must be between 2 and 6")

    templates = {
        "strength": {
            2: [("full_body", ["squat", "bench_press", "deadlift"]),
                ("full_body", ["overhead_press", "barbell_row", "lunges"])],
            3: [("push", ["bench_press", "overhead_press", "tricep_dips"]),
                ("pull", ["deadlift", "barbell_row", "pull_ups"]),
                ("legs", ["squat", "romanian_deadlift", "lunges"])],
            4: [("upper", ["bench_press", "barbell_row", "overhead_press"]),
                ("lower", ["squat", "romanian_deadlift", "calf_raises"]),
                ("upper", ["incline_bench_press", "pull_ups", "dumbbell_press"]),
                ("lower", ["deadlift", "front_squat", "leg_curl"])],
        },
        "hypertrophy": {
            2: [("upper", ["bench_press", "lat_pulldown", "shoulder_press"]),
                ("lower", ["squat", "leg_press", "leg_curl"])],
            3: [("push", ["bench_press", "incline_dumbbell_press", "lateral_raise"]),
                ("pull", ["barbell_row", "pull_ups", "bicep_curl"]),
                ("legs", ["squat", "leg_press", "leg_curl"])],
            4: [("chest_triceps", ["bench_press", "incline_bench_press", "tricep_pushdown"]),
                ("back_biceps", ["barbell_row", "lat_pulldown", "bicep_curl"]),
                ("legs", ["squat", "romanian_deadlift", "leg_press"]),
                ("shoulders_core", ["overhead_press", "lateral_raise", "plank"])],
        },
        "general_fitness": {
            2: [("full_body", ["goblet_squat", "push_ups", "dumbbell_row"]),
                ("full_body", ["romanian_deadlift", "plank", "walking_lunges"])],
            3: [("full_body", ["squat", "push_ups", "row"]),
                ("conditioning", ["kettlebell_swing", "burpees", "plank"]),
                ("full_body", ["deadlift", "dumbbell_press", "lunges"])],
            4: [("upper", ["push_ups", "dumbbell_press", "row"]),
                ("lower", ["squat", "lunges", "leg_curl"]),
                ("conditioning", ["bike", "burpees", "plank"]),
                ("full_body", ["deadlift", "overhead_press", "farmer_walk"])],
        },
    }

    available_days = sorted(templates[goal].keys())
    chosen_days = min(available_days, key=lambda x: abs(x - days_per_week))
    base_plan = templates[goal][chosen_days]

    volume_note_map = {
        "beginner": "Use 2-3 working sets per exercise and focus on technique.",
        "intermediate": "Use 3-4 working sets per exercise and apply progressive overload.",
        "advanced": "Use 4-5 working sets per exercise and manage fatigue carefully.",
    }

    adaptive_notes = []

    if plateau_summary.get("bench_press") == "High":
        adaptive_notes.append("Bench press plateau is high: reduce pressing fatigue and consider incline or dumbbell variation.")
    if plateau_summary.get("squat") == "High":
        adaptive_notes.append("Squat plateau is high: consider a lighter squat day or technique-focused variation.")
    if plateau_summary.get("deadlift") == "High":
        adaptive_notes.append("Deadlift plateau is high: reduce deadlift intensity and add posterior-chain accessory work.")

    if not adaptive_notes:
        adaptive_notes.append("No major plateau detected. Continue with the base plan.")

    plan = []
    for i, (focus, exercises) in enumerate(base_plan, start=1):
        adjusted_exercises = exercises.copy()

        if plateau_summary.get("bench_press") == "High" and "bench_press" in adjusted_exercises:
            adjusted_exercises = ["incline_bench_press" if ex == "bench_press" else ex for ex in adjusted_exercises]

        if plateau_summary.get("deadlift") == "High" and "deadlift" in adjusted_exercises:
            adjusted_exercises = ["romanian_deadlift" if ex == "deadlift" else ex for ex in adjusted_exercises]

        plan.append({
            "day": i,
            "focus": focus,
            "exercises": adjusted_exercises
        })

    return {
        "goal": goal,
        "days_per_week": days_per_week,
        "experience": experience,
        "plan": plan,
        "recommendation": volume_note_map[experience],
        "adaptive_notes": adaptive_notes,
        "plateau_summary": plateau_summary,
    }