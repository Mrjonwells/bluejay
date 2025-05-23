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
            kw_list=["credit card processing", "cash discount", "business loans", "merchant services"],
            timeframe='now 1-d'
        )
        data = pytrends.related_queries()
        trending = data["credit card processing"]["top"]
        return trending["query"][0]
    except Exception:
        print("[Fallback] Trending fetch failed: list index out of range")
        return "Smart Business Savings Strategy"

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
    if 'origin' not in [remote.name for remote in repo.remotes]:
        repo.create_remote('origin', os.environ["GIT_REMOTE"])
    repo.config_writer().set_value("user", "name", "BlueJay Bot").release()
    repo.config_writer().set_value("user", "email", "bot@askbluejay.ai").release()
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
    slug_base = title.lower().replace(" ", "_").replace("?", "").replace(",", "").replace("'", "")
    slug = f"{slug_base}_{datetime.now().strftime('%Y%m%d%H%M')}"
    body = f"""
Cash discount programs, optimized for modern businesses, offer an effective way to legally reduce transaction fees while enhancing customer loyalty. This strategy empowers your brand to pass processing costs transparently and boosts profitability.

AskBlueJay.ai automates this with intelligent savings and seamless compliance. Learn more today.
"""
    html = render_blog_html(title, body)
    save_blog_file(slug, html)
    update_blog_index(slug, title)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
