import json
import os
from datetime import datetime

LOG_PATH = "backend/logs/interaction_log.jsonl"
BRAIN_RECOMMENDATIONS_PATH = "backend/config/brain_update_recommendations.json"

FIELD_KEYWORDS = {
    "monthly_card_volume": ["monthly", "k", "processing", "10k", "15k", "20k", "volume"],
    "average_ticket": ["ticket", "avg", "average sale", "per transaction", "each sale"],
    "processor": ["square", "stripe", "clover", "paypal", "pos", "processor"],
    "transaction_type": ["online", "in person", "tap", "counter", "ecommerce"],
    "business_name": ["shop", "llc", "inc", "taco", "called", "named"],
    "contact_info": ["@", ".com", "email", "phone", "text", "reach me"]
}

def parse_logs():
    if not os.path.exists(LOG_PATH):
        print("No interaction log found.")
        return {}

    field_counts = {k: 0 for k in FIELD_KEYWORDS}
    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                user_input = entry.get("user", "").lower()
                for field, keywords in FIELD_KEYWORDS.items():
                    if any(kw.lower() in user_input for kw in keywords):
                        field_counts[field] += 1
            except Exception:
                continue
    return field_counts

def generate_recommendations(counts):
    recommendations = []
    for field, count in counts.items():
        if count < 3:
            recommendations.append(f"Low capture: '{field}' — improve detection or nudge questions.")
    return recommendations

def save_output(field_counts, recs):
    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "field_counts": field_counts,
        "recommendations": recs
    }
    os.makedirs(os.path.dirname(BRAIN_RECOMMENDATIONS_PATH), exist_ok=True)
    with open(BRAIN_RECOMMENDATIONS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print("✅ Brain update recommendations written.")

if __name__ == "__main__":
    counts = parse_logs()
    recs = generate_recommendations(counts)
    save_output(counts, recs)
