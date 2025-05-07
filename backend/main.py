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
r = redis.Redis.from_url(os.getenv("REDIS_URL"))

# Load BlueJay brain
brain_path = os.path.join("backend", "bluejay", "bluejay_config.json")
with open(brain_path, "r") as f:
    bluejay_brain = json.load(f)

# Log memory per thread
def get_thread_id(session_id):
    key = f"thread:{session_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = client.beta.threads.create()
    r.setex(key, 1800, new_thread.id)
    return new_thread.id

# Store interaction log
def log_interaction(session_id, user_input, assistant_reply):
    ts = int(time.time())
    log = {"ts": ts, "session_id": session_id, "input": user_input, "reply": assistant_reply}
    with open("backend/logs/interaction_log.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")

@app.route("/", methods=["GET"])
def index():
    return "<h1 style='color:white;background:black;text-align:center;padding:50px'>BlueJay backend is live!</h1>"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input received."})

    # Calendly trigger
    if any(x in user_input.lower() for x in ["book", "schedule", "call", "calendar"]):
        return jsonify({"reply": "Sure — grab a time here: https://calendly.com/askbluejay/30min"})

    session_id = request.remote_addr or str(uuid.uuid4())
    thread_id = get_thread_id(session_id)

    system_context = f"""
BlueJay is a business-savvy sales assistant. Use this config to guide your replies without repeating answered questions:

{json.dumps(bluejay_brain)}

You are smart, adaptive, and focused on moving the sale forward. Do not ask for info already gathered.
"""

    try:
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            instructions=system_context
        )

        while run.status not in ["completed", "failed", "cancelled"]:
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run.status != "completed":
            return jsonify({"reply": "Error during assistant run."})

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = next((m.content[0].text.value for m in messages.data if m.role == "assistant"), "...")
        log_interaction(session_id, user_input, reply)
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})
