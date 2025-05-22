import os
import re
import markdown2
from git import Repo, GitCommandError
from openai import OpenAI
from pytrends.request import TrendReq

REPO_URL = "https://github.com/Mrjonwells/bluejay.git"
BLOG_DIR = "frontend/blogs/"
BLOG_INDEX = "frontend/blog.html"

def fetch_trending_keywords():
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload(['merchant processing'], cat=0, timeframe='now 1-d', geo='US')
        related = pytrends.related_queries()
        keywords = related['merchant processing']['top']
        if keywords is None:
            raise IndexError("No related keywords returned.")
        return [kw['query'] for kw in keywords[:5]]
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return [
            "cash discount program",
            "credit card processing fees",
            "merchant services",
            "small business savings",
            "no fee processing"
        ]

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write an SEO-optimized blog post for small business owners about '{keyword}'. Include a title and helpful content."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def save_blog_to_file(title, content, slug):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <header>
    <img src="../logo.png" alt="BlueJay Logo" class="centered-logo" />
  </header>
  <section class="hero">
    <h1>{title}</h1>
  </section>
  <section class="chat-container">
    <div class="chatlog">
      {markdown2.markdown(content)}
    </div>
  </section>
</body>
</html>
"""
    filepath = os.path.join(BLOG_DIR, slug + ".html")
    with open(filepath, "w") as f:
        f.write(html_content)
    print(f"Blog saved to {filepath}")
    return filepath

def update_blog_index(slug, title, summary):
    entry = f"""<div class="blog-preview">
  <a href="blogs/{slug}.html"><strong>{title}</strong></a>
  <p>{summary}</p>
</div>\n"""
    with open(BLOG_INDEX, "r") as f:
        existing = f.read()
    if entry not in existing:
        with open(BLOG_INDEX, "a") as f:
            f.write(entry)
        print("Blog index updated")

def extract_title_and_summary(blog):
    lines = blog.split("\n")
    title = lines[0].replace("Title:", "").strip() if lines[0].lower().startswith("title:") else "Untitled"
    content = "\n".join(lines[1:]).strip()
    summary = content[:180] + "..." if len(content) > 180 else content
    return title, content, summary

def slugify(text):
    return re.sub(r'\W+', '_', text.lower()).strip('_')

def git_commit_and_push(slug):
    repo = Repo(os.getcwd())
    try:
        origin = repo.remote(name="origin")
    except ValueError:
        origin = repo.create_remote("origin", url=REPO_URL)

    try:
        if repo.head.is_detached:
            repo.git.checkout("-B", "main")
        repo.git.add(A=True)
        repo.index.commit(f"Add blog: {slug}")
        repo.git.push("--set-upstream", "origin", "main")
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    title, content, summary = extract_title_and_summary(blog)
    slug = slugify(title)
    save_blog_to_file(title, content, slug)
    update_blog_index(slug, title, summary)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
