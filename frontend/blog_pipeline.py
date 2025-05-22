import os
import openai
import json
import random
from datetime import datetime
from pytrends.request import TrendReq
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

pytrends = TrendReq(hl="en-US", tz=360)

BLOG_DIR = "frontend/blogs"
INDEX_PATH = "frontend/blog.html"

def fetch_trending_keywords():
    pytrends.build_payload(["merchant services", "credit card fees", "cash discount"], timeframe="now 7-d")
    related = pytrends.related_queries()
    keywords = []

    for topic in related.values():
        if topic and "top" in topic and topic["top"] is not None:
            for item in topic["top"].head(5).to_dict("records"):
                if "query" in item:
                    keywords.append(item["query"])

    if not keywords:
        print("No related keywords found — using fallback set.")
        keywords = ["merchant services 2025", "ai credit card processing", "small business fee savings"]

    return keywords

def generate_blog_content(topic):
    prompt = f"Write a helpful, engaging blog post for small business owners about '{topic}'. Use a human tone, include specific tips, and keep it under 500 words."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional blog writer for a fintech startup."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

def summarize_blog(blog_text):
    prompt = f"Summarize the following blog in one compelling sentence designed to hook readers:\n\n{blog_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def create_blog_file(title, content):
    filename = title.lower().replace(" ", "-").replace(".", "") + ".html"
    path = os.path.join(BLOG_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html = f"""<html><head><title>{title}</title></head><body><h1>{title}</h1><article>{content}</article></body></html>"""
    with open(path, "w") as f:
        f.write(html)
    return filename

def update_blog_index(entries):
    entries_html = []
    for entry in entries:
        title = entry["title"]
        filename = entry["filename"]
        summary = entry["summary"]
        entries_html.append(f'<div class="blog-entry"><a href="blogs/{filename}">{title}</a><p>{summary}</p></div>')

    full_html = f"""<html><head><title>BlueJay Blog</title></head><body><h1>BlueJay Blog</h1>{''.join(entries_html)}</body></html>"""
    with open(INDEX_PATH, "w") as f:
        f.write(full_html)

def main():
    keywords = fetch_trending_keywords()
    topic = random.choice(keywords)
    blog_content = generate_blog_content(topic)
    summary = summarize_blog(blog_content)
    title = topic.title()

    filename = create_blog_file(title, blog_content)
    update_blog_index([{"title": title, "filename": filename, "summary": summary}])
    print(f"Blog '{title}' generated successfully.")

if __name__ == "__main__":
    main()
