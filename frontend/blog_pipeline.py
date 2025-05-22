import os
import json
import random
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from pytrends.request import TrendReq

BLOG_DIR = Path("frontend/blogs")
INDEX_PATH = Path("frontend/blog.html")
DEFAULT_KEYWORDS = ["cash discounting", "merchant processing", "card fee elimination", "AI payment assistant"]

def fetch_trending_keywords():
    pytrends = TrendReq()
    pytrends.build_payload(["merchant services", "credit card processing", "business payments"], timeframe="now 7-d")
    try:
        related = pytrends.related_queries()
        keywords = []
        for key in related:
            ranked = related[key].get("top", {}).get("query", [])
            if ranked:
                keywords += ranked
        return keywords or DEFAULT_KEYWORDS
    except Exception as e:
        print("[Fallback] Trending fetch failed:", str(e))
        return DEFAULT_KEYWORDS

def generate_blog(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    today = datetime.now().strftime("%B %d, %Y")
    prompt = (
        f"Write an SEO-optimized blog post for small business owners on '{topic}'. "
        f"Include a catchy title, 2-3 paragraph overview, and highlight how AI-powered merchant processing (like AskBlueJay.ai) saves money. "
        f"Keep the tone helpful and clear. Include today's date: {today}."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def save_blog_file(title, content):
    filename = title.lower().replace(" ", "_").replace(".", "") + ".html"
    filepath = BLOG_DIR / filename
    html = f"""<html><head><title>{title}</title></head><body><h1>{title}</h1><p>{datetime.now().strftime("%B %d, %Y")}</p><article>{content}</article></body></html>"""
    with open(filepath, "w") as f:
        f.write(html)
    return filename, content[:180].strip().replace('\n', ' ') + "..."

def update_index(new_title, filename, preview):
    if not INDEX_PATH.exists():
        with open(INDEX_PATH, "w") as f:
            f.write("<html><head><title>BlueJay Blog</title></head><body><h1>BlueJay’s Blog</h1><div id='blogs'></div></body></html>")

    with open(INDEX_PATH, "r") as f:
        html = f.read()

    insert_point = html.find("</div>")
    if insert_point != -1:
        new_entry = f"<div><a href='blogs/{filename}'>{new_title}</a><p>{preview}</p></div>\n"
        html = html[:insert_point] + new_entry + html[insert_point:]

    with open(INDEX_PATH, "w") as f:
        f.write(html)

def main():
    keywords = fetch_trending_keywords()
    main_kw = random.choice(keywords)
    blog = generate_blog(main_kw)

    title_line = blog.split("\n")[0]
title = title_line.replace("Title:", "").strip("# ").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()

    filename, preview = save_blog_file(title, content)
    update_index(title, filename, preview)
    print(f"Blog '{title}' posted as {filename}")

if __name__ == "__main__":
    main()
