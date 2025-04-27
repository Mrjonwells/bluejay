import os
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# You don't need to load .env here, because the variables are coming from Railway
# load_dotenv()

app = Flask(__name__)
CORS(app)

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# The assistant ID for the OpenAI assistant
assistant_id = os.getenv("ASSISTANT_ID")


def get_thread_id(user_id):
    """
    Get the thread ID for the user from Redis.
    """
    thread_key = f"thread:{user_id}"
    thread_id = r.get(thread_key)
    if thread_id:
        return thread_id.decode("utf-8")
    else:
        return None


def save_thread_id(user_id, thread_id):
    """
    Save the thread ID for the user in Redis.
    """
    thread_key = f"thread:{user_id}"
    r.set(thread_key, thread_id)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "BlueJay API running."}), 200


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle incoming messages and pass them to OpenAI.
    """
    data = request.json
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400

    user_id = data.get("user_id", str(uuid.uuid4()))
    thread_id = get_thread_id(user_id)

    if not thread_id:
        # If no thread exists, create one.
        thread = client.beta.threads.create()
        thread_id = thread.id
        save_thread_id(user_id, thread_id)

    # Send user message to OpenAI thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )

    # Create a run for the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Poll until the assistant completes the run
    while True:
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        if run_check.status == "completed":
            break

    # Retrieve the latest message
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    latest_message = messages.data[0].content[0].text.value

    # Return the assistant's response
    return jsonify({"response": latest_message})


if __name__ == "__main__":
    # Dynamically bind to the port provided by Railway
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)