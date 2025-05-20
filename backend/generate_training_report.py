import json
import os
import requests
from datetime import datetime
from pathlib import Path

RECOMMENDATIONS_PATH = Path("backend/brain_update_recommendations.json")
REPORT_PATH = Path("backend/training_report.md")

MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
TO_EMAIL = os.environ.get("ADMIN_EMAIL")  # e.g. your email address
FROM_EMAIL = f"BlueJay Training <mailgun@{MAILGUN_DOMAIN}>"

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

    report_content = "\n".join(lines)

    with open(REPORT_PATH, "w") as out:
        out.write(report_content)

    print("Training report generated.")
    send_email(report_content)

def send_email(content):
    if not MAILGUN_DOMAIN or not MAILGUN_API_KEY or not TO_EMAIL:
        print("Missing Mailgun config. Email not sent.")
        return

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": FROM_EMAIL,
            "to": TO_EMAIL,
            "subject": "Daily Learning Summary",
            "text": content
        }
    )

    if response.status_code == 200:
        print("Daily learning summary sent.")
    else:
        print(f"Mailgun error: {response.status_code} — {response.text}")

if __name__ == "__main__":
    generate_report()
