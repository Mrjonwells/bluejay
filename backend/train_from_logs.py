import json
from pathlib import Path

LOG_PATH = Path("backend/logs/interaction_log.jsonl")
RECOMMENDATION_PATH = Path("backend/brain_update_recommendations.json")

def analyze_logs():
    recommendations = {"cash_discounting": [], "calendar_triggering": [], "seo_keywords": []}
    if not LOG_PATH.exists():
        print("No logs found.")
        return

    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                msg = entry.get("user", "").lower() + " " + entry.get("assistant", "").lower()
                if "cash discount" in msg or "zero fee" in msg:
                    recommendations["cash_discounting"].append("reinforce multi-step explanation")
                if "book" in msg or "meeting" in msg or "calendar" in msg:
                    recommendations["calendar_triggering"].append("reinforce calendly popup timing")
                if "seo" in msg or "search" in msg or "blog" in msg:
                    recommendations["seo_keywords"].append("log user search language")
            except:
                continue

    with open(RECOMMENDATION_PATH, "w") as out:
        json.dump(recommendations, out, indent=2)
    print("Updated recommendations saved.")

if __name__ == "__main__":
    analyze_logs()
