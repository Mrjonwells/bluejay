import os
import uuid
import redis
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# Load env vars
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

# Load brain
brain_path = os.path.join(os.path.dirname(__file__), "bluejay", "bluejay_config.json")
with open(brain_path) as f:
    config = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    user_id = data.get("user_id", str(uuid.uuid4()))

    if not user_input:
        return jsonify({"response": "Can you repeat that?"})

    try:
        # Retrieve or create thread
        thread_id = None
        if r:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()

        if not thread_id:
            thread = client.beta.threads.create()
            thread_id = thread.id
            if r:
                r.set(f"thread:{user_id}", thread_id)

        # Add user message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Run assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for completion
        while True:
            status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if status.status == "completed":
                break
            elif status.status in ["failed", "cancelled", "expired"]:
                return jsonify({"response": "Sorry, I ran into a snag processing that."})
            time.sleep(1)

        # Get assistant reply
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = None
        for msg in messages.data:
            if msg.role == "assistant":
                reply = msg.content[0].text.value.strip()
                break

        if not reply:
            reply = "Sorry, I didn’t catch that."

        return jsonify({"response": reply})

    except OpenAIError as e:
        print("OpenAI API error:", e)
        return jsonify({"response": "Error with OpenAI processing."})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"response": "Something went wrong on my end. Try again soon."})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
