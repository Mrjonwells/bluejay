import os
import re
import datetime
from openai import OpenAI
from pytrends.request import TrendReq
from git import Repo, GitCommandError
import markdown2

BLOG_DIR = "frontend/blogs/"
BLOG_INDEX = "frontend/blog.html"
REPO_PATH = os.getcwd()
REPO_URL = "https://github.com/Mrjonwells/bluejay.git"
BLUEJAY_PAT = os.getenv("BLUEJAY_PAT")

def fetch_trending_keywords():
    pytrends = TrendReq()
    try:
        pytrends.build_payload(["merchant processing"])
        related = pytrends.related_queries()
        keyword_data = related["merchant processing"]["top"]
        return [row["query"] for row in keyword_data.to_dict("records")][:5]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", str(e))
        return [
            "cash discount programs",
            "save on credit card fees",
            "merchant processing AI",
            "cut payment processing costs",
            "point of sale savings"
        ]

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a short blog post (3-5 paragraphs) for small business owners about '{keyword}', highlighting how cash discount programs help them save money on credit card processing fees. Make it clear, persuasive, and SEO-optimized with a compelling title."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

def slugify(title):
    return re.sub(r"\W+", "_", title.lower())

def save_blog(title, body, slug):
    content = "\n".join(body.split("\n")[1:]).strip()
    html = f"""<!DOCTYPE html>
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
  <section class="blog-post">
    <h1>{title}</h1>
    <p class="date">{datetime.date.today().strftime("%B %d, %Y")}</p>
    <p>{markdown2.markdown(content)}</p>
  </section>
  <footer>
    <p>BlueJay and AskBlueJay.ai are property of Fortified Capital LLC. All rights reserved.</p>
  </footer>
</body>
</html>"""

    path = os.path.join(BLOG_DIR, f"{slug}.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"Blog saved to {path}")

def update_index(slug, title, summary):
    with open(BLOG_INDEX, "r") as f:
        html = f.read()

    date_str = datetime.date.today().strftime("%B %d, %Y")
    snippet = f"""
    <div class="blog-snippet">
      <a href="blogs/{slug}.html">{title}</a>
      <p class="date">{date_str}</p>
      <p class="summary">{summary}</p>
    </div>
    """

    marker = "<!-- BLOG_INSERT -->"
    if marker in html:
        html = html.replace(marker, f"{snippet}\n{marker}")
    with open(BLOG_INDEX, "w") as f:
        f.write(html)
    print("Blog index updated")

def git_commit_and_push(slug):
    repo = Repo(REPO_PATH)
    repo.git.add(A=True)
    repo.index.commit(f"Add blog post: {slug}")
    try:
        repo.git.pull('--rebase')
        repo.remote(name="origin").push('--set-upstream', 'origin', 'main', env={
            "GIT_ASKPASS": "echo",
            "GIT_USERNAME": "bluejay",
            "GIT_PASSWORD": BLUEJAY_PAT
        })
        print("Blog pushed to GitHub.")
    except GitCommandError as e:
        print("[Git Push Error]", e)

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    lines = blog.split("\n")
    title = lines[0].replace("Title:", "").strip()
    slug = slugify(title)
    summary = " ".join(lines[1:3]).strip()
    save_blog(title, blog, slug)
    update_index(slug, title, summary)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
