import os
import json
import redis
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
LOG_DIR = "backend/logs/conversations/"
os.makedirs(LOG_DIR, exist_ok=True)

# Parse Redis URL to set SSL if using rediss://
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

def fetch_conversations():
    threads = {}
    for key in redis_client.scan_iter("thread:*"):
        try:
            data = redis_client.get(key)
            if data:
                threads[key] = json.loads(data)
        except Exception:
            continue
    return threads

def score_conversations(threads):
    scores = {}
    for thread_id, messages in threads.items():
        field_flags = {k: False for k in FIELD_KEYWORDS}
        for msg in messages:
            if msg["role"] != "user":
                continue
            content = msg["content"].lower()
            for field, keywords in FIELD_KEYWORDS.items():
                if any(kw.lower() in content for kw in keywords):
                    field_flags[field] = True
        score = sum(field_flags.values())
        scores[thread_id] = {
            "score": score,
            "missing": [field for field, found in field_flags.items() if not found]
        }
    return scores

def save_snapshot(threads, scores):
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(LOG_DIR, f"conversation_snapshot_{timestamp}.json")
    combined = {
        "timestamp": timestamp,
        "total_threads": len(threads),
        "thread_scores": scores,
        "threads": threads
    }
    with open(out_path, "w") as f:
        json.dump(combined, f, indent=2)
    print(f"Saved {len(threads)} threads to {out_path}")

if __name__ == "__main__":
    all_threads = fetch_conversations()
    all_scores = score_conversations(all_threads)
    save_snapshot(all_threads, all_scores)
