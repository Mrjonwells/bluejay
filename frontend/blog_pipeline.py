import os
import json
import time
import random
from datetime import datetime
from pathlib import Path
from pytrends.request import TrendReq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

pytrends = TrendReq(
    hl='en-US',
    tz=360,
    timeout=(10, 25),
    retries=3,
    backoff_factor=0.5,
    user_agent=random.choice(USER_AGENTS)
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

BLOG_DIR = Path("frontend/blogs/")
BLOG_INDEX = Path("frontend/blog.html")

SEO_KEYWORDS = ["merchant services", "credit card fees", "cash discount"]

def fetch_trending_keywords():
    all_keywords = []
    for keyword in SEO_KEYWORDS:
        try:
            pytrends.build_payload([keyword], timeframe="now 7-d")
            related = pytrends.related_queries()
            time.sleep(1.5)  # throttle
            if keyword in related:
                top = related[keyword].get("top")
                if top is not None:
                    terms = [x["query"] for x in top[:3]]
                    all_keywords.extend(terms)
        except Exception as e:
            print(f"Trend fetch failed for '{keyword}': {e}")
    return list(set(all_keywords))[:5]

def generate_blog(topic):
    print(f"Generating blog for topic: {topic}")
    prompt = f"Write a helpful blog post about '{topic}' for small business owners, focused on merchant processing, savings, and AI help. Include a catchy title and summary first."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def save_blog_post(title, body):
    safe_title = title.replace(" ", "_").replace("/", "-").lower()
    filename = f"{datetime.now().strftime('%Y-%m-%d')}_{safe_title}.html"
    filepath = BLOG_DIR / filename

    html_content = f"""<html><head><title>{title}</title></head>
    <body><h1>{title}</h1><div>{body.replace('\n', '<br>')}</div></body></html>"""

    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html_content)

    print(f"Saved: {filepath}")
    return filename, title, body[:150]

def update_blog_index(entries):
    index_lines = [
        "<html><head><title>BlueJay’s Blog</title></head><body>",
        "<h1>BlueJay’s Blog</h1><div style='font-family:sans-serif;'>"
    ]
    for filename, title, snippet in entries:
        index_lines.append(f"<p><a href='blogs/{filename}'><strong>{title}</strong></a><br>{snippet}...</p>")
    index_lines.append("</div></body></html>")

    with open(BLOG_INDEX, "w") as idx:
        idx.write("\n".join(index_lines))

def main():
    print("Blog pipeline started.")
    trends = fetch_trending_keywords()
    if not trends:
        print("No trending topics found.")
        return

    entries = []
    for topic in trends:
        try:
            blog = generate_blog(topic)
            lines = blog.split("\n")
            title = lines[0].strip("# ").strip()
            body = "\n".join(lines[1:]).strip()
            entry = save_blog_post(title, body)
            entries.append(entry)
            time.sleep(2)
        except Exception as e:
            print(f"Blog generation failed for '{topic}': {e}")

    if entries:
        update_blog_index(entries)
        print("Blog index updated.")
    else:
        print("No new blog entries saved.")

if __name__ == "__main__":
    main()
