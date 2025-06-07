import json
import os
import redis
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = "backend/logs/interaction_log.jsonl"
BRAIN_RECOMMENDATIONS_PATH = "backend/config/brain_update_recommendations.json"
REDIS_URL = os.getenv("REDIS_URL")

parsed_url = urllib.parse.urlparse(REDIS_URL)
use_ssl = parsed_url.scheme == "rediss"
redis_client = redis.from_url(REDIS_URL, ssl=use_ssl, decode_responses=True)

FIELD_KEYWORDS = {
    "monthly_card_volume": ["$10,000", "$15000", "75000", "20k", "monthly volume", "card sales", "processing", "$12000"],
    "average_ticket": ["average ticket", "ticket size", "typically spend", "avg sale", "$8", "$15", "$18"],
    "processor": ["Square", "Stripe", "Clover", "POS", "processor", "terminal", "using"],
    "transaction_type": ["online", "counter", "in person", "ecommerce", "website"],
    "business_name": ["LLC", "Inc", "taco shop", "company name", "we’re a coffee shop"],
    "contact_info": ["@gmail.com", "@yahoo.com", "@", "phone", "reach me"]
}

def parse_redis_threads():
    field_counts = {k: 0 for k in FIELD_KEYWORDS}
    for key in redis_client.scan_iter("thread:*"):
        try:
            messages = json.loads(redis_client.get(key))
            for msg in messages:
                if msg["role"] == "user":
                    content = msg["content"].lower()
                    for field, keywords in FIELD_KEYWORDS.items():
                        if any(kw.lower() in content for kw in keywords):
                            field_counts[field] += 1
        except Exception:
            continue
    return field_counts

def generate_recommendations(counts):
    return [f"Improve capture rate for '{field}' — too few logged mentions." for field, count in counts.items() if count < 3]

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
    counts = parse_redis_threads()
    recs = generate_recommendations(counts)
    save_output(counts, recs)
