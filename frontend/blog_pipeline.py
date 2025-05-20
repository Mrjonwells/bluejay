import os
import json
import openai
from datetime import datetime
from pytrends.request import TrendReq
from pathlib import Path

# Setup paths
BLOG_DIR = Path("frontend/blogs")
BLOG_HTML = Path("frontend/blog.html")
LOG_PATH = Path("backend/logs/interaction_log.jsonl")
BLOG_DIR.mkdir(parents=True, exist_ok=True)

# Setup OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

def extract_keywords_from_logs():
    keywords = {}
    if not LOG_PATH.exists():
        return []

    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                text = (entry.get("user", "") + " " + entry.get("assistant", "")).lower()
                for word in ["cash discount", "merchant", "clover", "fees", "savings", "square", "switching"]:
                    if word in text:
                        keywords[word] = keywords.get(word, 0) + 1
            except:
                continue

    return sorted(keywords, key=keywords.get, reverse=True)[:5]

def fetch_trending_keywords():
    pytrends = TrendReq()
    pytrends.build_payload(["merchant services", "credit card fees", "cash discount"], timeframe="now 7-d")
    related = pytrends.related_queries()
    trend_keywords = []

    for topic in related.values():
        if topic and topic["top"] is not None:
            trend_keywords += [row["query"] for row in topic["top"].head(5).to_dict("records")]

    return trend_keywords[:10]

def generate_title_and_post(topic):
    prompt = f"Write a short, engaging blog post for small business owners about '{topic}', highlighting value, savings, or switching processors. Title should be compelling, and content should sound natural and educational."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful blog assistant writing for a merchant payment company called BlueJay."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    full_text = response.choices[0].message["content"].strip()
    title = full_text.split("\n")[0].replace("#", "").strip()
    body = "\n".join(full_text.split("\n")[1:]).strip()

    return title, body

def save_blog_post(title, body):
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = "-".join(title.lower().split())[:40]
    filename = f"{date_str}_{slug}.md"
    path = BLOG_DIR / filename

    with open(path, "w") as f:
        f.write(f"# {title}\n\n{body}")

    print(f"Blog saved: {filename}")
    return filename, title, body

def extract_title_and_summary(md_path):
    with open(md_path, "r") as f:
        lines = f.readlines()

    title = "Untitled"
    summary = ""

    for line in lines:
        if line.startswith("# "):
            title = line.strip("# ").strip()
        elif line.strip():
            summary = line.strip()
            break

    return title, summary

def update_blog_index():
    blog_entries = []

    for md_file in sorted(BLOG_DIR.glob("*.md"), reverse=True):
        title, summary = extract_title_and_summary(md_file)
        filename = md_file.name.replace(".md", ".html")
        blog_entries.append(f"""
        <div class="blog-entry">
          <a href="blogs/{filename}">{title}</a>
          <p>{summary}</p>
        </div>
        """)

    html = f"""
    <html>
    <head>
      <title>BlueJay Blog</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <h1>BlueJay’s Blog</h1>
      <div class="blog-list">
        {''.join(blog_entries)}
      </div>
    </body>
    </html>
    """

    with open(BLOG_HTML, "w") as f:
        f.write(html.strip())

    print("Blog index updated.")

def main():
    topics_from_logs = extract_keywords_from_logs()
    trends = fetch_trending_keywords()
    candidates = topics_from_logs + trends

    if not candidates:
        candidates = ["cash discounting for merchants"]

    topic = candidates[0]
    title, body = generate_title_and_post(topic)
    save_blog_post(title, body)
    update_blog_index()

if __name__ == "__main__":
    main()
