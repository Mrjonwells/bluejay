import os
import time
import json
import re
from datetime import datetime
from pytrends.request import TrendReq
from openai import OpenAI
import subprocess

# ENV setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GIT_USER = os.getenv("GIT_USER", "bluejay-bot")
GIT_EMAIL = os.getenv("GIT_EMAIL", "bluejay@askbluejay.ai")

def fetch_trending_keywords():
    pytrends = TrendReq()
    try:
        pytrends.build_payload(["merchant services"], timeframe="now 7-d")
        related = pytrends.related_queries()
        for kw in related.values():
            try:
                return kw['top']['query'][0]
            except:
                continue
    except Exception as e:
        print("[Fallback] Trending fetch failed:", str(e))
    return "cash discount program"

def generate_blog(topic):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Write a short SEO-optimized blog post for small business owners about: {topic}. Include a compelling title and 2-3 paragraphs."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content):
    slug = re.sub(r'\W+', '_', title.lower()).strip("_")
    filename = f"{slug}.html"
    filepath = os.path.join("frontend", "blogs", filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <header>
    <a href="../index.html"><img src="../logo.png" class="centered-logo" alt="BlueJay Logo" /></a>
  </header>
  <main class="blog-post">
    <h1>{title}</h1>
    <p>{content.replace('\n', '</p><p>')}</p>
  </main>
  <footer>
    <p>BlueJay and AskBlueJay.ai are property of Fortified Capital LLC. All rights reserved.</p>
  </footer>
</body>
</html>""")
    return filename

def update_blog_index():
    blog_dir = os.path.join("frontend", "blogs")
    index_path = os.path.join("frontend", "blog.html")

    blog_links = []
    for fname in sorted(os.listdir(blog_dir), reverse=True):
        if fname.endswith(".html"):
            title = fname.replace("_", " ").replace(".html", "").title()
            blog_links.append(f'<div class="blog-entry"><a href="blogs/{fname}">{title}</a></div>')

    with open(index_path, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>BlueJay Blog</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header>
    <a href="index.html"><img src="logo.png" class="centered-logo" alt="BlueJay Logo" /></a>
  </header>
  <main class="blog-index">
    <h1>BlueJay’s Blog</h1>
    {''.join(blog_links)}
  </main>
  <footer>
    <p>BlueJay and AskBlueJay.ai are property of Fortified Capital LLC. All rights reserved.</p>
  </footer>
</body>
</html>""")

def git_commit_push():
    subprocess.run(["git", "config", "--global", "user.name", GIT_USER])
    subprocess.run(["git", "config", "--global", "user.email", GIT_EMAIL])
    subprocess.run(["git", "add", "frontend/blogs"])
    subprocess.run(["git", "add", "frontend/blog.html"])
    subprocess.run(["git", "commit", "-m", "Automated blog update"])
    subprocess.run(["git", "push"])

def main():
    topic = fetch_trending_keywords()
    blog = generate_blog(topic)
    title_line, content = blog.split("\n", 1)
    title = title_line.strip("Title: ").strip()
    filename = save_blog(title, content.strip())
    print(f"Blog saved to frontend/blogs/{filename}")
    update_blog_index()
    git_commit_push()
    print("Blog index updated and changes pushed to GitHub.")

if __name__ == "__main__":
    main()
