import os
import re
import markdown2
from git import Repo, GitCommandError, InvalidGitRepositoryError
from datetime import datetime
from pytrends.request import TrendReq
from openai import OpenAI

# Constants
BLOG_FOLDER = "frontend/blogs"
INDEX_FILE = "frontend/blog.html"
REPO_PATH = os.path.abspath(".")  # Use Git root
GIT_REMOTE = os.getenv("GIT_REMOTE")
GIT_TOKEN = os.getenv("BLUEJAY_PAT")

def fetch_trending_keyword():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list=["credit card processing", "merchant services", "cash discount"], timeframe='now 7-d', geo='US')
        trends = pytrends.related_queries()
        return trends["credit card processing"]["top"]["query"].iloc[0]
    except Exception:
        print("[Fallback] Trending fetch failed: list index out of range")
        return "Cash Discount Programs"

def generate_blog(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an SEO-optimized financial copywriter for merchant services."},
            {"role": "user", "content": f"Write a blog post about: '{topic}' with a clear headline, intro, and a few paragraphs for small business owners."}
        ]
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content):
    slug = re.sub(r'\W+', '_', title.lower()).strip('_')
    filename = f"{slug}.html"
    filepath = os.path.join(BLOG_FOLDER, filename)

    os.makedirs(BLOG_FOLDER, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"<html><head><title>{title}</title></head><body>")
        f.write(f"<h2>{title}</h2>")
        for para in content.split("\n"):
            if para.strip():
                f.write(f"<p>{para.strip()}</p>")
        f.write("</body></html>")

    print(f"Blog saved to {filepath}")
    return filename

def update_blog_index():
    files = sorted(os.listdir(BLOG_FOLDER), reverse=True)
    entries = []
    for file in files:
        if file.endswith(".html"):
            slug = file.replace(".html", "")
            title = slug.replace("_", " ").title()
            entries.append(f'<div><a href="blogs/{file}">{title}</a></div>')

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("<html><head><title>BlueJay Blog</title></head><body>")
        f.write("<h1>BlueJay’s Blog</h1>")
        f.writelines(entries)
        f.write("</body></html>")

    print("Blog index updated")

def git_commit_and_push(slug):
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remotes.origin
    except InvalidGitRepositoryError:
        print("[Git Error] Not a valid Git repo.")
        return
    except Exception as e:
        print(f"[Git Error] Repo setup failed: {e}")
        return

    try:
        origin.fetch()
        repo.git.pull("origin", "main")
    except GitCommandError as e:
        print(f"[Git Error] during setup: {e}")
        return

    repo.git.add(".")
    repo.index.commit(f"Add blog post: {slug}")
    try:
        origin.push()
        print("Git push successful")
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")

def main():
    keyword = fetch_trending_keyword()
    blog = generate_blog(keyword)

    lines = blog.split("\n")
    title = lines[0].replace("Title:", "").strip()
    content = "\n".join(lines[1:]).strip()

    file_name = save_blog(title, content)
    update_blog_index()
    git_commit_and_push(file_name.replace(".html", ""))

if __name__ == "__main__":
    main()
