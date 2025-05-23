import os
import json
from datetime import datetime
from git import Repo, GitCommandError
from pytrends.request import TrendReq

BLOG_FOLDER = "docs/blogs"
BLOG_INDEX = "docs/blogs/index.json"
BLOG_TEMPLATE = "docs/blog_template.html"

def get_trending_topic():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(
            kw_list=["merchant services", "payment processors", "business loans", "credit card fees"],
            timeframe='now 1-d'
        )
        data = pytrends.related_queries()
        trending = data["merchant services"]["top"]
        return trending["query"][0]
    except Exception:
        print("[Fallback] Trending fetch failed: list index out of range")
        return "Cash Discount Programs"

def load_template():
    with open(BLOG_TEMPLATE, "r") as f:
        return f.read()

def render_blog_html(title, body):
    template = load_template()
    return template.replace("{{TITLE}}", title)\
                   .replace("{{DATE}}", datetime.now().strftime("%B %d, %Y"))\
                   .replace("{{BODY}}", body)

def save_blog_file(slug, html):
    os.makedirs(BLOG_FOLDER, exist_ok=True)
    path = os.path.join(BLOG_FOLDER, f"{slug}.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"Blog saved to {path}")
    return path

def update_blog_index(slug, title):
    os.makedirs(os.path.dirname(BLOG_INDEX), exist_ok=True)
    index = []
    if os.path.exists(BLOG_INDEX):
        with open(BLOG_INDEX, "r") as f:
            index = json.load(f)
    entry = {
        "slug": slug,
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    index = [entry] + [e for e in index if e["slug"] != slug]
    with open(BLOG_INDEX, "w") as f:
        json.dump(index, f, indent=2)
    print("Blog index updated")

def git_commit_and_push(slug):
    repo = Repo(".")
    repo.git.config("--global", "user.name", "BlueJay Bot")
    repo.git.config("--global", "user.email", "bot@askbluejay.ai")
    try:
        repo.git.add(".")
        repo.git.commit("-m", f"Auto-blog update: {slug}")
    except GitCommandError:
        print("[Git] Nothing to commit.")
    try:
        repo.git.push("origin", "main")
        print("[Git Push] Blog committed and pushed.")
    except GitCommandError as e:
        print("[Git Push Error]", str(e))

def main():
    title = get_trending_topic()
    slug = title.lower().replace(" ", "_").replace("?", "").replace(",", "").replace("'", "")
    slug = f"{slug}_{datetime.now().strftime('%Y%m%d%H%M')}"
    body = f"""
Cash discount programs are transforming the way small businesses handle credit card fees. By offering a discount to customers who pay with cash, these programs help business owners increase profitability, manage expenses, and stay competitive.

Implementing a cash discount program is easy and legal in all 50 states. It also helps build stronger customer relationships and keeps more money in your pocket.

Visit AskBlueJay.ai to discover how your business can save big today.
"""
    html = render_blog_html(title, body)
    save_blog_file(slug, html)
    update_blog_index(slug, title)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
