from pathlib import Path


def merge_results(prediction_results: list[dict], plateau_results: list[dict]) -> list[dict]:
    """
    Merge prediction results and plateau detection results by exercise name.
    """
    plateau_map = {item["exercise"]: item for item in plateau_results}
    merged = []

    for pred in prediction_results:
        exercise = pred["exercise"]
        plateau = plateau_map.get(exercise, {})

        merged_item = {
            "exercise": exercise,
            "current_estimated_1rm": pred.get("current_estimated_1rm"),
            "predicted_4_week_1rm": pred.get("predicted_4_week_1rm"),
            "predicted_8_week_1rm": pred.get("predicted_8_week_1rm"),
            "plateau_risk": plateau.get("plateau_risk", "Unknown"),
            "reason": plateau.get("reason", "No reason available."),
        }
        merged.append(merged_item)

    return merged


def format_report(merged_results: list[dict]) -> str:
    """
    Format merged results into a readable text report.
    """
    lines = []
    lines.append("=" * 20 + " WORKOUT PROGRESS REPORT " + "=" * 20)
    lines.append("")

    for item in merged_results:
        lines.append(f"Exercise: {item['exercise']}")
        lines.append(f"Current estimated 1RM: {item['current_estimated_1rm']} kg")
        lines.append(f"Predicted 4-week 1RM: {item['predicted_4_week_1rm']} kg")
        lines.append(f"Predicted 8-week 1RM: {item['predicted_8_week_1rm']} kg")
        lines.append(f"Plateau risk: {item['plateau_risk']}")
        lines.append(f"Reason: {item['reason']}")
        lines.append("-" * 60)

    return "\n".join(lines)


def print_report(report_text: str) -> None:
    """
    Print the final report to terminal.
    """
    print(report_text)


def save_report(report_text: str, output_path: str = "outputs/reports/workout_report.txt") -> None:
    """
    Save the final report to a text file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)