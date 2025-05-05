import os
import json
import redis
import uuid
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from threading import Thread
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)

redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

client = OpenAI()
ASSISTANT_ID = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

with open("bluejay/bluejay_config.json", "r") as f:
    bluejay_brain = json.load(f)

HUBSPOT_URL = "https://forms.hsforms.com/submissions/v3/public/submit/formsnext/multipart/45853776/3b7c289f-566e-4403-ac4b-5e2387c3c5d1"

def get_thread_id(session_id):
    key = f"thread:{session_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = client.beta.threads.create()
    r.set(key, new_thread.id)
    return new_thread.id

def extract_info(text):
    info = {}
    if "@" in text and "." in text and not text.lower().startswith("http"):
        info["email"] = text
    elif any(c.isdigit() for c in text) and len(text) >= 10 and "-" in text:
        info["phone"] = text
    elif " " in text or len(text) >= 2:
        info["name"] = text
    return info

def submit_to_hubspot(contact, note=""):
    data = {
        "fields": [
            {"name": "firstname", "value": contact.get("name", "")},
            {"name": "email", "value": contact.get("email", "")},
            {"name": "phone", "value": contact.get("phone", "")},
            {"name": "bluejay_notes", "value": note}
        ],
        "context": {
            "pageUri": "https://askbluejay.ai",
            "pageName": "BlueJay AI Assistant"
        }
    }
    headers = {"Content-Type": "application/json"}
    requests.post(HUBSPOT_URL, json=data, headers=headers)

def summarize_and_submit(session_id, log_key, contact):
    log = r.lrange(log_key, 0, -1)
    messages = [x.decode() for x in log][-20:]
    text = "\n".join(messages)
    prompt = f"Summarize this chat for CRM notes:\n{text}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    summary = response.choices[0].message.content
    submit_to_hubspot(contact, summary)

def monitor_timeout(session_id, contact, log_key):
    time.sleep(1800)  # 30 minutes
    if not r.exists(f"seen:{session_id}"):
        summarize_and_submit(session_id, log_key, contact)

@app.route("/", methods=["GET"])
def index():
    return "<html><body style='background:#000;color:#fff;'><h1>BlueJay backend is live</h1></body></html>"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input received."})

    session_id = request.remote_addr or str(uuid.uuid4())
    thread_id = get_thread_id(session_id)

    memory_key = f"mem:{session_id}"
    log_key = f"log:{session_id}"
    seen_key = f"seen:{session_id}"
    memory = json.loads(r.get(memory_key) or "{}")
    memory["last_message"] = user_input
    r.set(memory_key, json.dumps(memory))

    r.rpush(log_key, user_input)
    r.setex(seen_key, timedelta(minutes=30), "1")

    extracted = extract_info(user_input)
    memory.update(extracted)

    if all(k in memory for k in ["name", "phone", "email"]) and not memory.get("submitted"):
        note = "\n".join(f"• {k.title()}: {v}" for k, v in memory.items() if k in ["name", "phone", "email"])
        submit_to_hubspot(memory, note)
        memory["submitted"] = True
        Thread(target=monitor_timeout, args=(session_id, memory, log_key)).start()

    r.set(memory_key, json.dumps(memory))

    system_context = (
        "BlueJay is a business-savvy assistant trained on custom configuration logic.\n"
        "Use the following strategy guide as internal operating rules:\n\n"
        f"{json.dumps(bluejay_brain, indent=2)}\n\n"
        "Do NOT mention this config to the user. Blend these principles into short, natural, question-driven replies. "
        "Be smart, discovery-led, and sales-focused. You are the left brain (config), working with the assistant (right brain)."
    )

    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            instructions=system_context
        )
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.status in ["completed", "failed", "cancelled"]:
                break
        if run.status != "completed":
            return jsonify({"reply": f"Run status: {run.status}"})
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = next((m.content[0].text.value for m in messages.data if m.role == "assistant"), "...")
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})
