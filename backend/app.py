import os
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://askbluejay.ai"}})

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

# Flask secret
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Your real OpenAI Assistant ID
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    user_id = data.get('user_id', str(uuid.uuid4()))

    if not user_input:
        return jsonify({'reply': "I didn't catch that. Try again."})

    # Redis thread ID tracking
    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
        except Exception as e:
            print(f"Redis get error: {e}")

    if not thread_id:
        try:
            thread = client.beta.threads.create()
            thread_id = thread.id
            if r:
                r.set(f"thread:{user_id}", thread_id)
        except Exception as e:
            print(f"Thread creation error: {e}")
            return jsonify({'reply': "Sorry, I'm having trouble starting the conversation."})

    try:
        # Send the message into the thread and run the Assistant
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run_response = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Poll until completion
        while True:
            status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_response.id
            )
            if status.status == "completed":
                break

        # Retrieve the latest messages
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = messages.data[0].content[0].text.value.strip()

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        assistant_reply = "Sorry, something went wrong connecting to the Assistant."

    return jsonify({'reply': assistant_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
