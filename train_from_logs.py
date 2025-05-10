import json
import os
from datetime import datetime

LOG_PATH = "backend/logs/interaction_log.jsonl"
BRAIN_RECOMMENDATIONS_PATH = "backend/config/brain_update_recommendations.json"

FIELD_KEYWORDS = {
    "monthly_card_volume": ["$10,000", "$15000", "75000", "20k", "monthly volume", "card sales", "processing"],
    "average_ticket": ["average ticket", "ticket size", "typically spend", "avg sale", "$8", "$15", "$18"],
    "processor": ["Square", "Stripe", "Clover", "POS", "processor", "terminal", "using"],
    "transaction_type": ["online", "counter", "in person", "ecommerce", "website"],
    "business_name": ["LLC", "Inc", "taco shop", "company name", "we’re a coffee shop"],
    "contact_info": ["@gmail.com", "@yahoo.com", "@", "phone", "reach me"]
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
            recommendations.append(f"Improve capture rate for '{field}' — too few logged mentions.")
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
    print("Recommendations written to brain_update_recommendations.json")

if __name__ == "__main__":
    counts = parse_logs()
    recs = generate_recommendations(counts)
    save_output(counts, recs)
