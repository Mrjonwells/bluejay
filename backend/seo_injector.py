from flask import Flask, request, jsonify
from flask_cors import CORS
from seo_injection import generate_blog_html  # assumes this exists
import os

app = Flask(__name__)
CORS(app)

@app.route("/seo/inject", methods=["POST"])
def inject_seo():
    data = request.get_json()
    topic = data.get("topic", "")
    if not topic:
        return jsonify({"error": "Missing topic"}), 400
    try:
        content, meta = generate_blog_html(topic)
        return jsonify({
            "topic": topic,
            "content": content,
            "meta": meta
        })
    except Exception as e:
        print("Injection error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
