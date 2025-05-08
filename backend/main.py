import os
import time
import redis
import requests
import json
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

r = redis.Redis.from_url(os.getenv("REDIS_URL"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

CONFIG_PATH = "backend/config/bluejay_config.json"
INTERACTION_LOG = "backend/logs/interaction_log.jsonl"

with open(CONFIG_PATH, "r") as f:
    bluejay_config = json.load(f)

def log_interaction(message):
    with open(INTERACTION_LOG, "a") as f:
        f.write(json.dumps(message) + "\n")
    print("Logged interaction.")

def get_thread_id(user_id):
    key = f"thread:{user_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = openai_client.beta.threads.create()
    r.setex(key, 1800, new_thread.id)
    return new_thread.id

def extract_fields(user_input):
    fields = {}
    input_lower = user_input.lower()
    shorthand = bluejay_config.get("shorthand_handling", {}).get("normalize", {})

    for k, v in shorthand.items():
        if k in input_lower:
            user_input = user_input.replace(k, v)

    for field in ["monthly_card_volume", "average_ticket"]:
        if "$" in user_input or "month" in user_input:
            try:
                fields[field] = int("".join(filter(str.isdigit, user_input)))
            except:
                pass

    for processor in ["Square", "Stripe", "Clover"]:
        if processor.lower() in input_lower:
            fields["processor"] = processor

    if any(word in input_lower for word in ["online", "web", "site"]):
        fields["transaction_type"] = "online"
    elif "in person" in input_lower or "counter" in input_lower:
        fields["transaction_type"] = "in-person"

    return fields

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    user_id = data.get("user_id", str(uuid.uuid4()))

    thread_id = get_thread_id(user_id)
    fields = extract_fields(user_input)

    for k, v in fields.items():
        r.setex(f"{user_id}:{k}", 1800, v)

    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=f"Use this config: {json.dumps(bluejay_config)}"
    )

    while True:
        run_status = openai_client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
    reply = next((msg.content[0].text.value for msg in reversed(messages.data) if msg.role == "assistant"), "Let me check on that.")

    log_interaction({
        "user_id": user_id,
        "input": user_input,
        "reply": reply,
        "fields": fields,
        "timestamp": time.time()
    })

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)