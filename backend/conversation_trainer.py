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

# Parse Redis URL to enable SSL if using rediss://
parsed_url = urllib.parse.urlparse(REDIS_URL)
use_ssl = parsed_url.scheme == "rediss"
redis_client = redis.from_url(REDIS_URL, ssl=use_ssl, decode_responses=True)

def fetch_and_dump_threads():
    logs = {}
    for key in redis_client.scan_iter("thread:*"):
        try:
            logs[key] = json.loads(redis_client.get(key))
        except Exception:
            continue

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(LOG_DIR, f"conversation_snapshot_{timestamp}.json")
    with open(out_path, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"Exported {len(logs)} threads to {out_path}")

if __name__ == "__main__":
    fetch_and_dump_threads()
