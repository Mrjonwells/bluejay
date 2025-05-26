import json
import random
import os

EXTERNAL_TOPICS_FILE = "backend/seo/external_topics.json"
BLOG_INDEX_FILE = "docs/blogs/index.json"

def get_trending_topic():
    try:
        with open(EXTERNAL_TOPICS_FILE, "r") as f:
            data = json.load(f)
            return random.choice(data.get("topics", []))
    except Exception as e:
        print("Fallback topic used:", e)
        return random.choice([
            "AI tools for small businesses",
            "Smart automation in eCommerce",
            "The future of remote teams in 2025"
        ])

def get_internal_links():
    try:
        with open(BLOG_INDEX_FILE, "r") as f:
            index = json.load(f)
            links = index[:3]
    except:
        links = []
    return links
