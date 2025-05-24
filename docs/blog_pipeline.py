import os
import json
from datetime import datetime
import requests
from jinja2 import Template

BLOG_FOLDER = "docs/blogs"
INDEX_FILE = "docs/blogs/index.json"
TEMPLATE_FILE = "docs/blogs/blog_template.html"
SEO_ENDPOINT = "https://bluejay-mjpg.onrender.com/seo/inject"
TREND_ENDPOINT = "https://bluejay-mjpg.onrender.com/seo/trending"

def fetch_trending_topic():
    try:
        res = requests.get(TREND_ENDPOINT)
        return res.json().get("rewritten_topic", "AI Trends in 2025")
    except Exception as e:
        print("Trending fetch error:", e)
        return "AI Trends in 2025"

def inject_seo(topic):
    try:
        res = requests.post(SEO_ENDPOINT, json={"topic": topic})
        body_html = res.json().get("content", "")
        meta = res.json().get("meta", {})
        print("Fetched content:", body_html[:60])
        print("Meta keys:", meta.keys())
        return body_html, meta
    except Exception as e:
        print("SEO injection error:", e)
        return "", {}

def render_post(topic, body_html, meta):
    with open(TEMPLATE_FILE) as f:
        template = Template(f.read())
    return template.render(
        title=topic,
        content=body_html,
        date=datetime.utcnow().strftime('%B %d, %Y'),
        meta=meta
    )

def save_post(filename, html):
    path = os.path.join(BLOG_FOLDER, filename)
    with open(path, "w") as f:
        f.write(html)

def update_index(title, filename, meta):
    index = []
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE) as f:
            index = json.load(f)
    index.insert(0, {
        "title": title,
        "filename": filename,
        "description": meta.get("description", ""),
        "keywords": meta.get("keywords", []),
        "date": datetime.utcnow().isoformat()
    })
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

def main():
    topic = fetch_trending_topic()
    body_html, meta = inject_seo(topic)
    slug = topic.lower().replace(" ", "-").replace("?", "")
    filename = f"{datetime.utcnow().strftime('%Y%m%d')}-{slug}.html"
    full_html = render_post(topic, body_html, meta)
    save_post(filename, full_html)
    update_index(topic, filename, meta)
    print("Index file updated at", datetime.utcnow())

if __name__ == "__main__":
    main()
