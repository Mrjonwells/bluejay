from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import redis
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Redis setup
r = redis.from_url(os.getenv("REDIS_URL"))

# OpenAI setup
client = OpenAI()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("user_input")

    if not user_input:
        return jsonify({"error": "Missing user input"}), 400

    try:
        # Here you would continue with the real thread/assistant logic
        assistant_reply = f"Hello! You said: {user_input}"

        return jsonify({"assistant": assistant_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)