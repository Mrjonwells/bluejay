import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Mailgun setup
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
TO_EMAIL = os.getenv("REPORT_TO_EMAIL", "you@yourdomain.com")
FROM_EMAIL = f"reports@{MAILGUN_DOMAIN}"

# Paths
LOG_PATH = "backend/logs/interaction_log.jsonl"
OBJECTION_LOG = "backend/logs/objection_log.jsonl"
RECS_PATH = "brain_update_recommendations.json"

def count_lines(path):
    try:
        with open(path, "r") as f:
            return sum(1 for _ in f)
    except:
        return 0

def generate_report():
    now = datetime.utcnow().strftime("%B %d, %Y %H:%M UTC")

    interactions = count_lines(LOG_PATH)
    objections = count_lines(OBJECTION_LOG)
    recs = count_lines(RECS_PATH)

    report = f"""BlueJay Daily Report — {now}

Interactions Today:      {interactions}
Objections Logged:       {objections}
AI Improvements Suggested: {recs}

Notes:
- Logs pulled from Redis thread memory and objection tracker.
- Improvements written to brain_update_recommendations.json
- New suggestions will be trained hourly.

Keep flying,
BlueJay Auto Systems
"""
    return report

def send_email(subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"BlueJay Reports <{FROM_EMAIL}>",
            "to": [TO_EMAIL],
            "subject": subject,
            "text": body
        }
    )

if __name__ == "__main__":
    report = generate_report()
    res = send_email("BlueJay Daily Report", report)
    print("Email sent:", res.status_code)
    print(res.text)
