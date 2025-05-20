import json
from datetime import datetime
from pathlib import Path

RECOMMENDATIONS_PATH = Path("backend/brain_update_recommendations.json")
REPORT_PATH = Path("backend/training_report.md")

def generate_report():
    if not RECOMMENDATIONS_PATH.exists():
        print("No recommendations to report.")
        return

    with open(RECOMMENDATIONS_PATH, "r") as f:
        data = json.load(f)

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [f"# BlueJay Training Report — {date_str}\n"]

    if data.get("cash_discounting"):
        lines.append("## Cash Discounting\n")
        for item in data["cash_discounting"]:
            lines.append(f"- {item}")

    if data.get("calendar_triggering"):
        lines.append("\n## Meeting Booking\n")
        for item in data["calendar_triggering"]:
            lines.append(f"- {item}")

    if data.get("seo_keywords"):
        lines.append("\n## SEO Signals\n")
        for item in data["seo_keywords"]:
            lines.append(f"- {item}")

    with open(REPORT_PATH, "w") as out:
        out.write("\n".join(lines))

    print("Training report generated.")

if __name__ == "__main__":
    generate_report()
