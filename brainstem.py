# brainstem.py

import redis
import json
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

# ⚠️ Fallback: strip SSL if unsupported
try:
    redis_client = redis.from_url(redis_url, decode_responses=True, ssl=True, ssl_cert_reqs=None)
except TypeError:
    redis_client = redis.from_url(redis_url, decode_responses=True)

def parse_redis_threads():
    threads = {}
    for key in redis_client.scan_iter("thread:*"):
        thread = redis_client.get(key)
        if thread:
            threads[key] = json.loads(thread)
    return threads

def generate_recommendations(thread_data):
    recs = {}
    for thread_id, messages in thread_data.items():
        if isinstance(messages, list) and len(messages) > 3:
            recs[thread_id] = "🧠 Suggest optimization: shorten greeting or vary closing."
    return recs

def save_output(counts, recs):
    with open("backend/logs/brain_output.json", "w") as f:
        json.dump({"counts": counts, "recommendations": recs}, f, indent=2)
