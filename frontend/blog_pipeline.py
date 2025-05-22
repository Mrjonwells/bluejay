import os
import re
import time
import markdown2
from openai import OpenAI
from pytrends.request import TrendReq
from git import Repo, GitCommandError

BLOG_DIR = "frontend/blogs/"
INDEX_FILE = "frontend/blog.html"
REPO_URL = f"https://{os.getenv('BLUEJAY_PAT')}@github.com/Mrjonwells/bluejay.git"

def fetch_trending_keywords():
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload(kw_list=["credit card processing"])
        related = pytrends.related_queries()
        queries = related.get("credit card processing", {}).get("top", {})
        if not queries or 'query' not in queries:
            raise IndexError("Empty query list")
        return [q["query"] for q in queries["query"]]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", e)
        return [
            "cash discount program",
            "eliminate processing fees",
            "merchant savings",
            "credit card surcharge",
            "POS system AI"
        ]

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a helpful blog post about {keyword} targeted at small business owners. Use clear language and focus on benefits."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def slugify(title):
    return re.sub(r"[^a-zA-Z0-9]+", "_", title.strip().lower())

def save_blog(title, content, slug):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <article class="blog-post">
    <h1>{title}</h1>
    {markdown2.markdown(content)}
  </article>
</body>
</html>
"""
    with open(os.path.join(BLOG_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Blog saved to {BLOG_DIR}{slug}.html")

def update_index(slug, title, summary):
    if not os.path.exists(INDEX_FILE):
        base = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>BlueJay’s Blog</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <h1 style="text-align:center;color:#00aaff;">BlueJay’s Blog</h1>
  <section id="blog-list" class="blog-list"></section>
</body>
</html>"""
        with open(INDEX_FILE, "w") as f:
            f.write(base)

    with open(INDEX_FILE, "r+", encoding="utf-8") as f:
        html = f.read()
        new_entry = f"""<div class="blog-preview">
  <a href="blogs/{slug}.html"><strong>{title}</strong></a>
  <p>{summary}</p>
</div>
"""
        updated = html.replace("</section>", new_entry + "\n</section>")
        f.seek(0)
        f.write(updated)
        f.truncate()
    print("Blog index updated")

def git_commit_and_push(slug):
    repo = Repo(os.getcwd())
    try:
        origin = repo.remote(name="origin")
    except ValueError:
        origin = repo.create_remote("origin", url=REPO_URL)

    try:
        repo.git.checkout("main")
    except GitCommandError as e:
        print(f"[Git Checkout Error] {e}")

    try:
        repo.git.add(A=True)
        repo.index.commit(f"Add blog: {slug}")
        origin.push()
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    title = blog.split("\n")[0].replace("Title:", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()
    slug = slugify(title)
    summary = content.split("\n")[0][:160]
    save_blog(title, content, slug)
    update_index(slug, title, summary)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
