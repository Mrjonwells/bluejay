import os
import json
import redis

# Safe Redis client init (avoids ssl error in certain environments)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(redis_url, decode_responses=True, ssl=True, ssl_cert_reqs=None)
except TypeError:
    redis_client = redis.from_url(redis_url, decode_responses=True)

def fetch_conversations():
    conversations = []
    try:
        for key in redis_client.scan_iter("thread:*"):
            raw = redis_client.get(key)
            if raw:
                conversations.append(json.loads(raw))
    except redis.RedisError as e:
        print("Redis error:", e)
    return conversations

def summarize_conversation(conv):
    # Placeholder logic — refine as needed
    return {"summary": f"Found {len(conv)} messages."}

def train_from_conversations(conversations):
    summaries = []
    for conv in conversations:
        summaries.append(summarize_conversation(conv))
    return summaries

def save_output(summaries):
    os.makedirs("backend/logs", exist_ok=True)
    with open("backend/logs/conversation_summaries.json", "w") as f:
        json.dump(summaries, f, indent=2)

if __name__ == "__main__":
    all_threads = fetch_conversations()
    if not all_threads:
        print("No threads found or Redis connection issue.")
    else:
        result = train_from_conversations(all_threads)
        save_output(result)
        print("✅ Saved summaries.")
