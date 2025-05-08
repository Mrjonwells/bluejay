import json
from collections import defaultdict, Counter
import os

LOG_PATH = "backend/logs/interaction_log.jsonl"
BRAIN_PATH = "backend/config/bluejay_config.json"
RECOMMENDATION_PATH = "backend/logs/brain_update_recommendations.json"

def load_logs():
    if not os.path.exists(LOG_PATH):
        print("No log file found.")
        return []
    with open(LOG_PATH, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def analyze_logs(logs):
    field_hits = defaultdict(list)
    deal_stage_terms = defaultdict(Counter)

    for entry in logs:
        memory = entry.get("memory", {})
        reply = entry.get("assistant_reply", "").lower()
        user_input = entry.get("user_input", "").lower()

        # Track field triggers
        for key in memory:
            field_hits[key].append(user_input)

        # Score by tone
        for stage, keywords in [
            ("curious", ["what", "how", "interested", "learn", "explore"]),
            ("qualified", ["volume", "rate", "square", "stripe", "provider", "ticket"]),
            ("stalling", ["later", "busy", "not now", "think", "circle back"]),
            ("closing", ["ready", "signup", "send", "move forward", "lock", "finish"])
        ]:
            for word in keywords:
                if word in user_input or word in reply:
                    deal_stage_terms[stage][word] += 1

    return {
        "field_usage": {k: len(v) for k, v in field_hits.items()},
        "deal_stage_terms": {k: dict(v.most_common(10)) for k, v in deal_stage_terms.items()}
    }

def save_recommendations(data):
    with open(RECOMMENDATION_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Recommendations written to {RECOMMENDATION_PATH}")

if __name__ == "__main__":
    logs = load_logs()
    if logs:
        insights = analyze_logs(logs)
        save_recommendations(insights)
    else:
        print("No logs to analyze.")
