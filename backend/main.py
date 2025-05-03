import os
import time
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

r = redis.from_url(os.getenv("REDIS_URL"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    thread_id = data.get("thread_id")

    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id

    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(0.5)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    reply = messages.data[0].content[0].text.value if messages.data else "..."

    # Memory expiry
    r.setex(f"thread:{thread_id}", 600, "active")
    return jsonify({"reply": reply, "thread_id": thread_id})

if __name__ == "__main__":
    app.run(debug=True)
