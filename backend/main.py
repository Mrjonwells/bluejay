import os
import time
import json
import redis
import uuid
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

# Redis
r = redis.from_url(os.getenv("REDIS_URL"))

# Config + Template paths
CONFIG_PATH = "config/bluejay_config.json"
TEMPLATE_PATH = "config/conversation_template.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
with open(TEMPLATE_PATH, "r") as f:
    convo_template = json.load(f)

# Flask
app = Flask(__name__)
CORS(app)

# Memory length (30 min)
MEMORY_TTL = 60 * 30

def get_thread_id(session_id):
    redis_key = f"thread:{session_id}"
    thread_id = r.get(redis_key)
    if thread_id:
        return thread_id.decode()
    new_thread = openai.beta.threads.create()
    r.setex(redis_key, MEMORY_TTL, new_thread.id)
    return new_thread.id

def log_interaction(user_input, assistant_response):
    with open("logs/interaction_log.jsonl", "a") as log:
        log.write(json.dumps({
            "user": user_input,
            "assistant": assistant_response,
            "timestamp": time.time()
        }) + "\n")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id", str(uuid.uuid4()))
    user_input = data["message"]

    thread_id = get_thread_id(session_id)
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    response = openai.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=f"""Use this config: {json.dumps(config)}.
And this sales flow as your guide: {json.dumps(convo_template)}.
Move the deal forward like a pro.""",
    )

    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    final = next((m for m in reversed(messages.data) if m.role == "assistant"), None)

    log_interaction(user_input, final.content[0].text.value)
    return jsonify({"reply": final.content[0].text.value})

@app.route("/")
def index():
    return jsonify({"status": "BlueJay backend active."})

if __name__ == "__main__":
    app.run(debug=True)
