import os
import redis
import uuid
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)
CORS(app)

# Environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
redis_url = os.getenv("REDIS_URL")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")

# Redis setup
r = redis.from_url(redis_url)

# OpenAI client setup
client = OpenAI(api_key=openai_api_key)

# Flask secret
app.secret_key = flask_secret_key or "supersecret"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_input = data.get("user_input")

        if not user_input:
            return jsonify({"error": "Missing user input"}), 400

        # Use or generate user ID
        user_id = request.headers.get("X-User-Id")
        if not user_id:
            user_id = str(uuid.uuid4())

        # Redis thread tracking
        thread_key = f"thread:{user_id}"
        thread_id = r.get(thread_key)

        if not thread_id:
            thread = client.beta.threads.create()
            thread_id = thread.id
            r.set(thread_key, thread_id, ex=1800)  # 30 mins
        else:
            thread_id = thread_id.decode()

        # Add user message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Run assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Wait for run to complete
        status = None
        for _ in range(20):
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            status = run_status.status
            if status == "completed":
                break
            time.sleep(1)

        if status != "completed":
            return jsonify({"error": "Assistant timed out"}), 500

        # Get latest assistant message
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_message = None
        for message in reversed(messages.data):
            if message.role == "assistant":
                assistant_message = message.content[0].text.value
                break

        if not assistant_message:
            return jsonify({"error": "No assistant response"}), 500

        return jsonify({"assistant": assistant_message})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return Response("BlueJay backend is running.", status=200, mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)