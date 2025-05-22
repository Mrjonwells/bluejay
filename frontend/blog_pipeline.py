import os
import re
import json
from datetime import datetime
from pytrends.request import TrendReq
from openai import OpenAI
from pathlib import Path

BLOG_DIR = Path("frontend/blogs/")
INDEX_FILE = Path("frontend/blog.html")

def fetch_trending_keywords():
    pytrends = TrendReq()
    try:
        pytrends.build_payload(["merchant services", "cash discount", "credit card processing"], timeframe="now 7-d")
        related = pytrends.related_queries()
        keywords = []

        for kw in related.values():
            if kw and "top" in kw:
                for entry in kw["top"].to_dict("records"):
                    if entry["query"].lower() not in keywords:
                        keywords.append(entry["query"].lower())

        return keywords[:5]

    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return [
            "cash discount program",
            "zero fee processing",
            "merchant service savings",
            "switch from square",
            "credit card surcharges"
        ]

def generate_blog(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""
Write a compelling SEO-optimized blog post titled "Title: {topic.title()}". 
Make it engaging for small business owners. Include a title line, a hook intro, and 3 short paragraphs. 
Use a helpful, professional tone. Don’t include markdown or HTML.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

def sanitize_filename(title):
    return re.sub(r"[^\w\-]", "_", title.lower()).replace(" ", "_")

def save_blog(title, content):
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(title) + ".html"
    blog_path = BLOG_DIR / filename

    html = "<html><head><title>{}</title></head><body><h2>{}</h2>".format(title, title)
    html += "".join(f"<p>{line.strip()}</p>" for line in content.split("\n") if line.strip())
    html += "</body></html>"

    with open(blog_path, "w") as f:
        f.write(html)

    update_blog_index(title, filename, content)

def update_blog_index(title, filename, content):
    date = datetime.now().strftime("%B %d, %Y")
    hook = content.split("\n")[0].strip()
    block = f"""
<div class="blog-preview">
  <a href="blogs/{filename}">{title}</a>
  <div class="blog-date">{date}</div>
  <div class="blog-hook">{hook}</div>
</div>
"""

    if not INDEX_FILE.exists():
        with open(INDEX_FILE, "w") as f:
            f.write("<html><head><title>BlueJay Blog</title></head><body>\n<h1>BlueJay’s Blog</h1>\n")

    with open(INDEX_FILE, "a") as f:
        f.write(block + "\n")

def main():
    keywords = fetch_trending_keywords()
    if not keywords:
        print("No keywords found.")
        return

    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    title_line = blog.split("\n")[0].replace("Title:", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()
    save_blog(title_line, content)
    print(f"Blog '{title_line}' posted as {sanitize_filename(title_line)}.html")

if __name__ == "__main__":
    main()
