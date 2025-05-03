import os
import re
import uuid
import redis
import json
import random
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

# Load BlueJay brain
brain_path = os.path.join(os.path.dirname(__file__), "bluejay", "bluejay_config.json")
with open(brain_path) as f:
    config = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()
        user_id = data.get("user_id", str(uuid.uuid4()))

        if not user_input:
            return jsonify({"reply": "Can you repeat that?"})

        # Redis thread management
        thread_id = r.get(f"thread:{user_id}") if r else None
        if thread_id:
            thread_id = thread_id.decode()
        else:
            thread = client.beta.threads.create()
            thread_id = thread.id
            if r:
                r.set(f"thread:{user_id}", thread_id)

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        while True:
            status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if status.status == "completed":
                break

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = messages.data[0].content[0].text.value.strip()

        if not reply:
            reply = "Sorry, I didn’t catch that."

        print("Assistant reply:", reply)  # DEBUG

        return jsonify({"reply": reply})

    except Exception as e:
        print("Chat error:", str(e))
        return jsonify({"reply": "Something went wrong on my end. Try again soon."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
