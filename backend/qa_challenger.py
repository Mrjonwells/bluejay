import json
import os
import redis
import urllib.parse
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = "backend/logs/interaction_log.jsonl"
OUTPUT_PATH = "backend/config/brain_update_recommendations.json"
REDIS_URL = os.getenv("REDIS_URL")

parsed_url = urllib.parse.urlparse(REDIS_URL)
use_ssl = parsed_url.scheme == "rediss"
redis_client = redis.from_url(REDIS_URL, ssl=use_ssl, decode_responses=True)

openai = OpenAI()

def extract_weak_responses():
    suggestions = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                log = json.loads(line)
                if log.get("quality") == "weak":
                    suggestions.append({
                        "thread_id": log.get("thread_id"),
                        "question": log.get("user_input"),
                        "answer": log.get("assistant_reply")
                    })
            except Exception:
                continue
    return suggestions

def recommend_improvements(suggestions):
    improvements = []
    for item in suggestions:
        prompt = f"Improve this weak response:\nQ: {item['question']}\nA: {item['answer']}"
        improved = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        new_reply = improved.choices[0].message.content
        improvements.append({
            "thread_id": item["thread_id"],
            "original": item["answer"],
            "improved": new_reply
        })
    return improvements

if __name__ == "__main__":
    suggestions = extract_weak_responses()
    if suggestions:
        updates = recommend_improvements(suggestions)
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w") as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "improvements": updates
            }, f, indent=2)
        print(f"Generated {len(updates)} improvement recommendations.")
    else:
        print("No weak responses found.")
