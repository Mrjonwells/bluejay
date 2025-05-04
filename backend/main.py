import os
import uuid
import redis
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

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

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            additional_instructions=json.dumps(config)
        )

        while True:
            status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if status.status == "completed":
                break
            elif status.status in ["failed", "cancelled", "expired"]:
                return jsonify({"response": "Sorry, I had trouble handling that."})
            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for m in messages.data:
            if m.role == "assistant":
                return jsonify({"response": m.content[0].text.value.strip()})

        return jsonify({"response": "No reply found, can you rephrase that?"})

    except OpenAIError as e:
        print("OpenAI error:", e)
        return jsonify({"response": "Trouble reaching my brain — try again in a sec."})
    except Exception as e:
        print("General error:", e)
        return jsonify({"response": "Hmm, I hit a snag. Try once more?"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)