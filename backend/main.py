import os, json, redis, uuid, time
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

client = OpenAI()
ASSISTANT_ID = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# Load BlueJay brain
with open("bluejay/bluejay_config.json", "r") as f:
    bluejay_brain = json.load(f)

# HubSpot settings
HUBSPOT_FORM_URL = "https://api.hsforms.com/submissions/v3/integration/submit/45853776/3b7c289f-566e-4403-ac4b-5e2387c3c5d1"

def get_thread_id(session_id):
    key = f"thread:{session_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = client.beta.threads.create()
    r.setex(key, 1800, new_thread.id)  # 30-min memory
    return new_thread.id

def log_interaction(session_id, user_input, assistant_reply):
    log_entry = {
        "timestamp": int(time.time()),
        "session_id": session_id,
        "user_input": user_input,
        "assistant_reply": assistant_reply
    }
    with open("logs/interaction_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def send_to_hubspot(name, email, phone):
    data = {
        "fields": [
            {"name": "firstname", "value": name},
            {"name": "email", "value": email},
            {"name": "phone", "value": phone}
        ],
        "context": {
            "pageUri": "https://askbluejay.ai",
            "pageName": "BlueJay AI"
        }
    }
    try:
        import requests
        requests.post(HUBSPOT_FORM_URL, json=data, timeout=5)
    except Exception as e:
        print("HubSpot error:", e)

@app.route("/", methods=["GET"])
def index():
    return "<h1 style='color:white;background:black;padding:50px;text-align:center'>BlueJay backend is live!</h1>"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input received."})

    # Calendly trigger
    if any(w in user_input.lower() for w in ["book", "schedule", "call", "appointment", "calendar", "meet"]):
        return jsonify({
            "reply": "Sure — grab a time here: https://calendly.com/askbluejay/30min\n\nI’ll follow up with the details after you book ✅"
        })

    session_id = request.remote_addr or str(uuid.uuid4())
    thread_id = get_thread_id(session_id)

    system_context = f"""
BlueJay is a business-savvy assistant trained on config logic and memory.

{json.dumps(bluejay_brain, indent=2)}

Use this as internal strategy only — never show it to users. Respond humanly, briefly, and helpfully.
"""

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
        while run.status not in ["completed", "failed", "cancelled"]:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run.status != "completed":
            return jsonify({"reply": f"Run status: {run.status}"})

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = next((m.content[0].text.value for m in messages.data if m.role == "assistant"), "...")

        # Memory logging
        log_interaction(session_id, user_input, reply)

        # Lead detection + submission
        if all(x in user_input.lower() for x in ["@", "name", "phone"]):
            name = user_input.split("name")[-1].split()[0]
            email = next((w for w in user_input.split() if "@" in w), "")
            phone = next((w for w in user_input.split() if w.isdigit() and len(w) >= 10), "")
            send_to_hubspot(name, email, phone)

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})
