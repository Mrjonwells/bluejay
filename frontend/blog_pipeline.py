import os
import json
import random
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq
from pathlib import Path

client = OpenAI()

BLOG_DIR = Path("frontend/blogs/")
INDEX_PATH = Path("frontend/blog.html")
SUMMARY_LOG = Path("frontend/blog_summary_log.json")

def fetch_trending_keywords():
    pytrends = TrendReq()
    pytrends.build_payload(["merchant services", "credit card fees", "cash discount"], timeframe="now 7-d")

    try:
        related = pytrends.related_queries()
        keywords = []
        for topic in related.values():
            if topic and topic.get("top"):
                for item in topic["top"]["query"]:
                    keywords.append(item)
        if not keywords:
            raise IndexError
        return list(set(keywords))[:10]
    except Exception:
        return [
            "cash discount program",
            "credit card fees",
            "merchant processing",
            "switch from Square",
            "save on Stripe fees",
            "Clover setup",
            "0% processing",
            "AI payment tools",
            "small biz savings",
            "tap to pay terminals"
        ]

def generate_blog_post(topic):
    prompt = f"Write a detailed blog post (3–5 paragraphs) for small business owners about '{topic}', focused on merchant processing, AI savings, or fee reduction. Use a professional, helpful tone."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def extract_summary(post):
    prompt = f"Summarize this blog post in one powerful, human-style hook: {post}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content, summary):
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace("’", "").replace("'", "")
    filename = f"{date_str}-{slug}.html"
    filepath = BLOG_DIR / filename

    with open(filepath, "w") as f:
        f.write(f"<h1>{title}</h1>\n<p><em>{date_str}</em></p>\n<p>{summary}</p>\n<hr>\n<p>{content}</p>")

    with open(SUMMARY_LOG, "a") as log:
        json.dump({"date": date_str, "title": title, "summary": summary, "file": filename}, log)
        log.write("\n")

    return filename, summary

def update_blog_index():
    posts = []
    for file in sorted(BLOG_DIR.glob("*.html"), reverse=True):
        date_str = file.name[:10]
        title = file.name[11:-5].replace("-", " ").title()
        with open(file) as f:
            lines = f.readlines()
            summary = ""
            for line in lines:
                if "<p>" in line and not summary:
                    summary = line.strip()
            posts.append((title, date_str, summary, file.name))

    with open(INDEX_PATH, "w") as idx:
        idx.write("<html><head><title>BlueJay Blog</title></head><body>\n")
        idx.write("<h1>BlueJay Blog</h1>\n")
        for title, date_str, summary, fname in posts:
            idx.write(f"<div><a href='blogs/{fname}'><strong>{title}</strong></a><br>")
            idx.write(f"<small>{date_str}</small><br>{summary}</div><hr>\n")
        idx.write("</body></html>")

def main():
    keywords = fetch_trending_keywords()
    topic = random.choice(keywords)
    blog = generate_blog_post(topic)
    summary = extract_summary(blog)
    filename, short_summary = save_blog(topic.title(), blog, summary)
    update_blog_index()
    print(f"Blog generated and saved as {filename}")

if __name__ == "__main__":
    main()
