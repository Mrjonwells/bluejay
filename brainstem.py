# bluejay/brainstem.py

import os
import json
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
import redis

# === Load Environment ===
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
TO_EMAIL = os.getenv("TO_EMAIL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Parse Redis with SSL support ===
parsed_url = urllib.parse.urlparse(REDIS_URL or "")
use_ssl = parsed_url.scheme == "rediss"
REDIS_CLIENT = redis.from_url(REDIS_URL, ssl=use_ssl, decode_responses=True)

# === Paths ===
LOG_PATH = "backend/logs/interaction_log.jsonl"
RECOMMENDATIONS_PATH = "backend/config/brain_update_recommendations.json"

# === Shared Field Keywords for User Intent Detection ===
FIELD_KEYWORDS = {
    "monthly_card_volume": ["$10,000", "$15000", "75000", "20k", "monthly volume", "card sales", "processing", "$12000"],
    "average_ticket": ["average ticket", "ticket size", "typically spend", "avg sale", "$8", "$15", "$18"],
    "processor": ["Square", "Stripe", "Clover", "POS", "processor", "terminal", "using"],
    "transaction_type": ["online", "counter", "in person", "ecommerce", "website"],
    "business_name": ["LLC", "Inc", "taco shop", "company name", "we’re a coffee shop"],
    "contact_info": ["@gmail.com", "@yahoo.com", "@", "phone", "reach me"]
}

# === Metadata Utils (optional, for timestamps or logs) ===
def timestamp():
    return datetime.utcnow().isoformat()

# === Validation (can be expanded) ===
def check_integrity():
    assert REDIS_URL, "Missing REDIS_URL"
    assert MAILGUN_API_KEY, "Missing MAILGUN_API_KEY"
    assert MAILGUN_DOMAIN, "Missing MAILGUN_DOMAIN"
    assert TO_EMAIL, "Missing TO_EMAIL"
    assert OPENAI_API_KEY, "Missing OPENAI_API_KEY"

# === Optional: patch downstream files dynamically (future)
# def sync_downstream_configs():
#     with open("backend/shared_constants.py", "w") as f:
#         f.write(f'FIELD_KEYWORDS = {json.dumps(FIELD_KEYWORDS, indent=2)}\n')

if __name__ == "__main__":
    check_integrity()
    print("✅ brainstem.py loaded and validated.")
