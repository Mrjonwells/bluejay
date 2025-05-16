import os
import json
import pytz
from datetime import datetime
import requests

# Load env variables
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
REPORT_RECIPIENT = os.getenv("REPORT_RECIPIENT", "jonathanwells@gmail.com")

# Log path
LOG_PATH = "backend/logs/interaction_log.jsonl"

def load_logs(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def summarize(logs):
    total_conversations = len(logs)
    total_messages = sum(len(entry.get("messages", [])) for entry in logs)
    avg_messages = round(total_messages / total_conversations, 2) if total_conversations else 0

    # Placeholder for future investor-facing metrics
    estimated_closings = round(total_conversations * 0.15)  # 15% conversion est.
    avg_response_time = "N/A"  # future logic can calculate this

    return {
        "conversations": total_conversations,
        "messages": total_messages,
        "average_messages": avg_messages,
        "estimated_closings": estimated_closings,
        "avg_response_time": avg_response_time
    }

def format_report(summary, report_time):
    return f"""
BlueJay Daily Report — {report_time}

Total Conversations: {summary['conversations']}
Total Messages Exchanged: {summary['messages']}
Avg. Messages per Conversation: {summary['average_messages']}
Estimated Closings (15%): {summary['estimated_closings']}
Avg. Response Time: {summary['avg_response_time']}

Investor Note: BlueJay is actively scaling engagement. These numbers reflect real merchant conversations in motion.

– BlueJay
"""

def send_email(subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"BlueJay Reports <reports@{MAILGUN_DOMAIN}>",
            "to": REPORT_RECIPIENT,
            "subject": subject,
            "text": body
        }
    )

def run_report():
    logs = load_logs(LOG_PATH)
    summary = summarize(logs)

    # Format time for Los Angeles
    la_time = datetime.now(pytz.timezone("America/Los_Angeles"))
    report_time = la_time.strftime("%B %d, %Y — %I:%M %p %Z")

    subject = f"BlueJay Daily Report – {report_time}"
    body = format_report(summary, report_time)

    response = send_email(subject, body)
    print(f"Email sent: {response.status_code}")

if __name__ == "__main__":
    run_report()
