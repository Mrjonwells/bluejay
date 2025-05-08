import json
from collections import Counter, defaultdict

LOG_PATH = "backend/logs/interaction_log.jsonl"
BRAIN_UPDATE_PATH = "backend/bluejay/brain_update_recommendations.json"

def load_logs():
    with open(LOG_PATH, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def extract_patterns(logs):
    keywords = Counter()
    objections = Counter()
    fallbacks = Counter()
    field_keys = Counter()

    for entry in logs:
        msg = entry.get("user_input", "").lower()
        reply = entry.get("assistant_reply", "").lower()
        memory = entry.get("memory", {})

        for word in msg.split():
            keywords[word] += 1

        if "not interested" in msg or "already have" in msg:
            objections[msg] += 1

        if reply in [
            "Want to take the next step or circle back later?",
            "Still thinking? I can simplify it for you."
        ]:
            fallbacks[reply] += 1

        for k in memory.keys():
            field_keys[k] += 1

    return {
        "common_keywords": keywords.most_common(15),
        "frequent_objections": objections.most_common(5),
        "fallback_usage": fallbacks.most_common(5),
        "frequent_memory_fields": field_keys.most_common(10)
    }

def save_recommendations(data):
    with open(BRAIN_UPDATE_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Brain update recommendations saved to {BRAIN_UPDATE_PATH}")

if __name__ == "__main__":
    logs = load_logs()
    patterns = extract_patterns(logs)
    save_recommendations(patterns)
