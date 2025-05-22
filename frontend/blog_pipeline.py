import os
import re
import datetime
import markdown2
from dotenv import load_dotenv
from pytrends.request import TrendReq
from openai import OpenAI
from git import Repo

load_dotenv()

pytrends = TrendReq(hl='en-US', tz=360)

FALLBACK_KEYWORDS = ["cash discount", "merchant services", "credit card processing"]
BLOG_FOLDER = "frontend/blogs/"
BLOG_INDEX = "frontend/blog.html"

def fetch_trending_keywords():
    try:
        pytrends.build_payload(FALLBACK_KEYWORDS, timeframe="now 7-d")
        related = pytrends.related_queries()
        keywords = []
        for kw in FALLBACK_KEYWORDS:
            if kw in related and related[kw]["top"] is not None:
                keywords.extend(related[kw]["top"]["query"].tolist()[:2])
        return list(set(keywords)) or FALLBACK_KEYWORDS
    except Exception as e:
        print("[Fallback] Trending fetch failed:", e)
        return FALLBACK_KEYWORDS

def generate_blog(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a helpful and engaging blog post for small business owners about: '{topic}'. Keep it SEO-optimized and informative."
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a professional business blog writer."},
                  {"role": "user", "content": prompt}],
        max_tokens=800
    )
    return completion.choices[0].message.content.strip()

def slugify(text):
    return re.sub(r"[^\w\-]", "_", text.lower().replace(" ", "_"))

def save_blog(title, content):
    slug = slugify(title)
    filename = f"{BLOG_FOLDER}{slug}.html"
    content_paragraphs = "".join(f"<p>{line}</p>" for line in content.split("\n") if line.strip())

    with open(filename, "w") as f:
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
    <a href="../index.html"><img src="../logo.png" alt="BlueJay Logo" class="centered-logo" /></a>
  </header>
  <main>
    <h1>{title}</h1>
    {content_paragraphs}
  </main>
  <footer>
    <p>BlueJay and AskBlueJay.ai are property of Fortified Capital LLC. All rights reserved.</p>
  </footer>
</body>
</html>""")
    return slug, filename

def update_blog_index(slug, title):
    if not os.path.exists(BLOG_INDEX):
        return

    with open(BLOG_INDEX, "r") as f:
        lines = f.readlines()

    with open(BLOG_INDEX, "w") as f:
        for line in lines:
            if "<!-- BLOG_ENTRIES -->" in line:
                f.write(line)
                f.write(f"""    <div class="blog-entry">
      <a href="blogs/{slug}.html">{title}</a><br />
      <p class="summary">A fresh perspective from BlueJay on {title}.</p>
    </div>\n""")
            else:
                f.write(line)

def git_commit_and_push(slug):
    repo = Repo(".")
    repo.git.add(A=True)
    repo.index.commit(f"Add blog: {slug}")
    repo.remote(name='origin').push(env={
        "GIT_ASKPASS": "echo",
        "GIT_USERNAME": "BlueJay",
        "GIT_PASSWORD": os.getenv("BLUEJAY_PAT")
    })

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    title = blog.split("\n")[0].replace("Title: ", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()
    slug, filepath = save_blog(title, content)
    print("Blog saved to", filepath)
    update_blog_index(slug, title)
    print("Blog index updated")
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
