import os
from datetime import datetime
from pathlib import Path
import markdown2
from pytrends.request import TrendReq
from openai import OpenAI
from git import Repo

# Constants
BLOG_FOLDER = Path(__file__).parent / "blogs"
INDEX_FILE = Path(__file__).parent / "blog.html"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure blog folder exists
BLOG_FOLDER.mkdir(exist_ok=True)

def fetch_trending_keywords():
    try:
        pytrends = TrendReq()
        pytrends.build_payload(["credit card processing"], timeframe='now 1-d')
        related = pytrends.related_queries()
        return list(related.values())[0]['top']['query'].tolist()
    except Exception:
        print("[Fallback] Trending fetch failed: list index out of range")
        return ["cash discount", "merchant processing", "small business savings"]

def generate_blog(topic):
    prompt = f"Write a helpful SEO blog post for small business owners about '{topic}' focusing on saving money using a cash discount program. Include title and 2-3 paragraphs."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content):
    safe_title = title.lower().replace(" ", "_").replace(":", "").replace("'", "")
    filename = f"{safe_title}.html"
    path = BLOG_FOLDER / filename

    html = (
        "<html><head>"
        f"<title>{title}</title>"
        "</head><body>"
        f"<h2>{title}</h2>"
        + "".join(f"<p>{line}</p>" for line in content.split("\n") if line.strip())
        + "</body></html>"
    )

    with open(path, "w") as f:
        f.write(html)

    print(f"Blog saved to {path}")
    return filename

def update_index(new_file, title):
    lines = []
    if INDEX_FILE.exists():
        with open(INDEX_FILE) as f:
            lines = f.readlines()

    now = datetime.now().strftime("%B %d, %Y")
    new_entry = f'<div><a href="blogs/{new_file}">{title}</a><br><small>{now}</small></div>\n'

    # Preserve header if exists, then add
    header = "<!DOCTYPE html>\n<html>\n<head><title>BlueJay Blog</title></head>\n<body>\n"
    footer = "</body></html>\n"
    body = [line for line in lines if "<body>" in line or "<div>" in line]

    with open(INDEX_FILE, "w") as f:
        f.write(header)
        for line in body:
            f.write(line)
        f.write(new_entry)
        f.write(footer)

    print("Blog index updated")

def git_commit_and_push(slug):
    repo_path = Path(__file__).resolve().parent
    repo = Repo(repo_path)

    if 'origin' not in [remote.name for remote in repo.remotes]:
        origin_url = os.getenv("GIT_REMOTE_URL")
        if not origin_url:
            print("[Git Error] Missing GIT_REMOTE_URL in environment.")
            return
        repo.create_remote('origin', origin_url)

    try:
        repo.git.pull('origin', 'main')
    except Exception as e:
        print(f"[Git Error] during setup: {e}")

    repo.git.add('--all')
    repo.index.commit(f"Add new blog post: {slug}")
    try:
        repo.remote(name='origin').push()
    except Exception as e:
        print(f"[Git Push Error] {e}")

def main():
    keywords = fetch_trending_keywords()
    topic = keywords[0] if keywords else "cash discount program"
    blog = generate_blog(topic)
    title = blog.split("\n")[0].replace("Title:", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()

    file_name = save_blog(title, content)
    update_index(file_name, title)
    git_commit_and_push(file_name.replace(".html", ""))

if __name__ == "__main__":
    main()
