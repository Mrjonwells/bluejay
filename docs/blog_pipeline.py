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
        pytrends.build_payload(kw_list=[
            "credit card processing",
            "cash discount",
            "business loans",
            "merchant services"
        ], timeframe='now 1-d')
        data = pytrends.related_queries()
        trending = data["cash discount"]["top"]
        return trending["query"][0]
    except Exception:
        print("[Fallback] Trending fetch failed: list index out of range")
        return "Cash Discount Programs"

def load_template():
    with open(BLOG_TEMPLATE, "r") as f:
        return f.read()

def render_blog_html(title, body):
    template = load_template()
    return template.replace("{{TITLE}}", title).replace("{{DATE}}", datetime.now().strftime("%B %d, %Y")).replace("{{BODY}}", body)

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

    # Set Git identity
    repo.config_writer().set_value("user", "name", "Jonathan").release()
    repo.config_writer().set_value("user", "email", "info@askbluejay.ai").release()

    # Ensure remote exists
    origin_url = os.environ.get("GIT_REMOTE")
    if "origin" not in [r.name for r in repo.remotes]:
        repo.create_remote("origin", origin_url)

    try:
        repo.git.add(".")
        repo.git.commit("-m", f"Auto-blog update: {slug}")
    except GitCommandError:
        print("[Git] Nothing to commit.")
    try:
        repo.git.push("origin", "main", "--force")
        print("[Git Push] Blog committed and pushed.")
    except GitCommandError as e:
        print("[Git Push Error]", str(e))

def main():
    title = get_trending_topic()
    slug = title.lower().replace(" ", "_").replace("?", "").replace(",", "").replace("'", "")
    body = f"""
Cash discount programs help small businesses save on processing fees by offering customers discounts for paying with cash. This approach not only boosts your bottom line but builds trust and loyalty. Discover how to legally implement and promote a program tailored to your customers.

Learn more at AskBlueJay.ai.
"""
    html = render_blog_html(title, body)
    save_blog_file(slug, html)
    update_blog_index(slug, title)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
