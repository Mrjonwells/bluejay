# backend/memory_manager.py

import redis
import json
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
SESSION_TTL_SECONDS = 1800  # 30 minutes

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def load_memory(user_id):
    try:
        raw = redis_client.get(user_id)
        if raw:
            memory = json.loads(raw)
            timestamp = memory.get("timestamp", 0)
            if time.time() - timestamp < SESSION_TTL_SECONDS:
                return memory
            else:
                redis_client.delete(user_id)  # expired
    except Exception as e:
        print("Memory load error:", e)

    return None  # start fresh


def save_memory(user_id, data):
    memory = {
        "timestamp": time.time(),
        "data": data
    }
    try:
        redis_client.set(user_id, json.dumps(memory), ex=SESSION_TTL_SECONDS)
    except Exception as e:
        print("Memory save error:", e)


def clear_memory(user_id):
    try:
        redis_client.delete(user_id)
    except Exception as e:
        print("Memory clear error:", e)


def generate_greeting(user_id):
    memory = load_memory(user_id)
    if not memory:
        return "Hi, I’m BlueJay, your merchant AI expert. What’s your name?"
    
    return "Welcome back — ready to pick up where we left off?"
