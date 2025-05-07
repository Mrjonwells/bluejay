import os, json, redis, uuid, datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

# Core setup
client = OpenAI()
ASSISTANT_ID = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)
interaction_log_path = "backend/logs/interaction_log.jsonl"

# Load brain
with open("backend/bluejay/bluejay_config.json", "r") as f:
    bluejay_brain = json.load(f)

# HubSpot info
HUBSPOT_FORM_URL = "https://api.hsforms.com/submissions/v3/integration/submit/45853776/3b7c289f-566e-4403-ac4b-5e2387c3c5d1"
HUBSPOT_TOKEN = os.getenv("HUBSPOT_TOKEN")

def get_thread_id(session_id):
    key = f"thread:{session_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = client.beta.threads.create()
    r.set(key, new_thread.id, ex=1800)  # 30-minute memory
    return new_thread.id

def log_interaction(session_id, user_input, assistant_reply):
    log = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "session_id": session_id,
        "user_input": user_input,
        "assistant_reply": assistant_reply
    }
    with open(interaction_log_path, "a") as f:
        f.write(json.dumps(log) + "\n")

def extract_lead_info(messages):
    text = " ".join(m.content[0].text.value for m in messages.data if m.role == "user").lower()
    info = {}
    if "@" in text:
        for word in text.split():
            if "@" in word and "." in word:
                info["email"] = word.strip(",.")
    for word in text.split():
        if word.isdigit() and len(word) == 10:
            info["phone"] = word
    if "name" not in info:
        name_line = next((m.content[0].text.value for m in messages.data if "name" in m.content[0].text.value.lower()), None)
        if name_line:
            info["name"] = name_line.split()[-1]
    return info if "email" in info and "phone" in info else None

def submit_to_hubspot(lead):
    payload = {
        "fields": [
            {"name": "email", "value": lead.get("email", "")},
            {"name": "phone", "value": lead.get("phone", "")},
            {"name": "firstname", "value": lead.get("name", "BlueJay User")}
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUBSPOT_TOKEN}"
    }
    try:
        requests.post(HUBSPOT_FORM_URL, headers=headers, json=payload)
    except Exception as e:
        print("HubSpot submission error:", e)

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
BlueJay is a business-savvy assistant trained on custom configuration logic.
{json.dumps(bluejay_brain, indent=2)}
Do NOT mention this config. Blend it into short, helpful, discovery-led replies. You are the config (left brain) working with the assistant (right brain).
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

        # Log to file
        log_interaction(session_id, user_input, reply)

        # Submit lead if info is complete
        lead = extract_lead_info(messages)
        if lead:
            submit_to_hubspot(lead)

        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": "Error: " + str(e)})
