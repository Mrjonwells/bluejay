import os
import json
import random
from openai import OpenAI
from datetime import datetime, timedelta

MODIFIERS = [
    "from a futuristic lens", "as a marketing trend", "with real-world examples",
    "using contrarian opinions", "explained like you're 5", "in a myth-vs-fact format",
    "as a short guide for small business owners", "for remote teams in 2025",
    "with an economic forecast twist", "through the lens of AI ethics",
    "as a startup launch playbook", "with metaphors and analogies",
    "in a step-by-step breakdown", "for Gen Z consumers",
    "using current 2025 events", "as an SEO strategy",
    "compared across industries", "in the style of a tutorial",
    "with recent Google Trends examples", "exploring long-term impact"
]

USED_INDEX = "docs/blogs/index.json"
TOPIC_FILE = "backend/seo/external_topics.json"

def get_trending_topic():
    all_topics = []
    try:
        with open(TOPIC_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                all_topics = data
            elif isinstance(data, dict) and "topics" in data:
                all_topics = [{"rewritten_topic": t} for t in data["topics"]]
    except Exception as e:
        print("Error loading topics:", e)

    if not all_topics:
        return {"rewritten_topic": "How Smart Merchants Are Scaling with AI"}

    used_titles = set()
    try:
        if os.path.exists(USED_INDEX):
            with open(USED_INDEX, "r") as f:
                index_data = json.load(f)
                cutoff = datetime.utcnow() - timedelta(days=365)
                used_titles = {
                    entry["title"] for entry in index_data
                    if "title" in entry and "date" in entry and datetime.fromisoformat(entry["date"]) > cutoff
                }
    except Exception as e:
        print("Error loading used index:", e)

    fresh_topics = [t for t in all_topics if t["rewritten_topic"] not in used_titles]
    if fresh_topics:
        return random.choice(fresh_topics)

    return random.choice(all_topics)

def generate_blog_content(payload):
    topic = payload.get("topic", "Latest Tech Trends")
    modifier = random.choice(MODIFIERS)
    model = "gpt-3.5-turbo-0125"  # ✅ Quota-safe model with high limits

    system_prompt = (
        "You are a professional blog writer generating original, SEO-optimized long-form posts (300–500+ words). "
        "Avoid reused phrases or intros. The post must be unique, readable, and topic-specific with internal linking hints."
    )

    user_prompt = (
        f"Write a long-form blog post about: '{topic}' — but {modifier}. "
        "Avoid listicles or recycled intros. Include one internal link reference to 'https://askbluejay.ai/blog.html'. "
        "Include proper structure: headings, bullet points if useful, and engaging sub-sections."
    )

    print(f"[INFO] Using model: {model}")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1.1
    )

    return {
        "content": response.choices[0].message.content.strip(),
        "meta": {
            "description": topic,
            "keywords": [w for w in topic.lower().split() if len(w) > 3]
        },
        "model": model
    }
