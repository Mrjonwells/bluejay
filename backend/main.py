import os, json, redis, uuid, time, requests
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

CONFIG_PATH = "backend/config/bluejay_config.json"
TEMPLATE_PATH = "backend/config/conversation_template.json"
LOG_PATH = "backend/logs/interaction_log.jsonl"
HUBSPOT_URL = "https://api.hsforms.com/submissions/v3/integration/submit/45853776/3b7c289f-566e-4403-ac4b-5e2387c3c5d1"

with open(CONFIG_PATH, "r") as f:
    bluejay_brain = json.load(f)
with open(TEMPLATE_PATH, "r") as f:
    sales_template = json.load(f)

def get_thread_id(session_id):
    key = f"thread:{session_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = client.beta.threads.create()
    r.set(key, new_thread.id, ex=1800)
    return new_thread.id

def store_fields(session_id, message):
    fields = {
        "monthly_card_volume": ["$", "monthly", "volume", "sales"],
        "average_ticket": ["ticket", "average sale"],
        "processor": ["square", "stripe", "clover"],
        "business_name": ["business is", "company name", "we are"],
        "transaction_type": ["in-person", "online", "store", "website"],
        "email": ["@", "email"],
        "phone": ["call", "phone", "text"]
    }
    for k, triggers in fields.items():
        if any(t in message.lower() for t in triggers):
            r.set(f"{session_id}:{k}", message.strip(), ex=1800)

def extract_memory(session_id):
    return {
        k.decode().split(":", 1)[1]: v.decode()
        for k in r.scan_iter(f"{session_id}:*")
        for v in [r.get(k)]
    }

@app.route("/", methods=["GET"])
def index():
    return "<h1 style='color:white;background:black;padding:50px;text-align:center'>BlueJay backend is live!</h1>"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input received."})

    session_id = request.remote_addr or str(uuid.uuid4())

    if any(word in user_input.lower() for word in ["book", "calendar", "schedule", "appointment", "meeting"]):
        return jsonify({"reply": "Grab a time here: https://calendly.com/askbluejay/30min"})

    thread_id = get_thread_id(session_id)
    store_fields(session_id, user_input)
    memory = extract_memory(session_id)

    system_context = f"""
BlueJay is a persuasive, human-style merchant advisor.
Reference this sales flow:

{json.dumps(sales_template, indent=2)}

Internal config:

{json.dumps(bluejay_brain)}

Memory from this lead:

{json.dumps(memory, indent=2)}

Ask smart discovery questions to guide toward a closed deal.
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

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = next((m.content[0].text.value for m in messages.data if m.role == "assistant"), "...")

        with open(LOG_PATH, "a") as log:
            log.write(json.dumps({
                "session_id": session_id,
                "timestamp": time.time(),
                "user_input": user_input,
                "assistant_reply": reply,
                "memory": memory
            }) + "\n")

        if all(r.get(f"{session_id}:{k}") for k in ["business_name", "monthly_card_volume", "average_ticket"]):
            payload = {
                "fields": [
                    {"name": "email", "value": r.get(f"{session_id}:email") or "n/a"},
                    {"name": "firstname", "value": r.get(f"{session_id}:business_name") or "Business"},
                    {"name": "phone", "value": r.get(f"{session_id}:phone") or "n/a"},
                    {"name": "message", "value": json.dumps(memory)}
                ]
            }
            try:
                requests.post(HUBSPOT_URL, json=payload, timeout=4)
            except:
                pass

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})
