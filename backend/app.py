import os
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Redis
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# OpenAI
client = OpenAI()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    user_id = data.get("user_id") or str(uuid.uuid4())
    thread_key = f"thread:{user_id}"

    thread_id = r.get(thread_key)
    if thread_id:
        thread_id = thread_id.decode("utf-8")
    else:
        thread = client.beta.threads.create()
        thread_id = thread.id
        r.set(thread_key, thread_id)

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
    )

    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    last_message = messages.data[0].content[0].text.value

    return jsonify({"response": last_message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)