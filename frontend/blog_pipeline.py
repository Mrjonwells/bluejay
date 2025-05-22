import os
import re
import time
import requests
from datetime import datetime
from pytrends.request import TrendReq
from openai import OpenAI
from git import Repo
from dotenv import load_dotenv

load_dotenv()

BLOG_DIR = "frontend/blogs"
INDEX_FILE = "frontend/blog.html"
REPO_PATH = os.getcwd()
GITHUB_PAT = os.getenv("BLUEJAY_PAT")
REPO_URL = "https://github.com/Mrjonwells/bluejay.git"

def fetch_trending_keywords():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(['credit card processing'], cat=0, timeframe='now 7-d', geo='', gprop='')
        related = pytrends.related_queries()
        kw_list = list(related['credit card processing']['top']['query'])[:5]
        return kw_list
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return [
            "cash discount processing",
            "credit card fee savings",
            "how to cut merchant fees",
            "merchant cash discount programs",
            "eliminate credit card fees"
        ]

def slugify(title):
    return re.sub(r'[\W_]+', '_', title.lower()).strip("_")

def generate_blog(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a blog post (~400 words) for small business owners about '{topic}' with a compelling title. Focus on saving money via credit card processing cash discount programs. Start with the title on the first line."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def save_blog(title, content):
    slug = slugify(title)
    filename = os.path.join(BLOG_DIR, f"{slug}.html")

    html_content = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\">\n"
        f"  <title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"  <h2>{title}</h2>\n"
        f"  <p>{content.replace(chr(10), '</p><p>')}</p>\n"
        "</body>\n"
        "</html>"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Blog saved to {filename}")
    return slug

def update_blog_index():
    entries = []
    for file in sorted(os.listdir(BLOG_DIR), reverse=True):
        if file.endswith(".html"):
            path = os.path.join(BLOG_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                title_line = f.readline()
                title = re.sub(r"<.*?>", "", title_line)
                hook = f.readline().strip()
                entries.append(f'<div class="blog-entry"><a href="blogs/{file}">{title}</a><p>{hook}</p></div>')

    index_html = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "  <title>BlueJay Blog</title>\n"
        "  <link rel=\"stylesheet\" href=\"style.css\" />\n"
        "</head>\n"
        "<body>\n"
        "  <header><h1>BlueJay’s Blog</h1></header>\n"
        "  <section class=\"blog-list\">\n"
        f"{''.join(entries)}\n"
        "  </section>\n"
        "</body>\n"
        "</html>"
    )

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Blog index updated")

def git_commit_and_push(slug):
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remotes.origin

        # Ensure tracking setup
        if repo.head.is_detached:
            print("Repo is in detached HEAD state. Skipping push.")
            return

        if repo.active_branch.tracking_branch() is None:
            repo.git.branch('--set-upstream-to=origin/main', 'main')

        repo.git.add(A=True)
        repo.index.commit(f"Add blog post: {slug}")
        origin.push()
        print("Pushed to GitHub")
    except Exception as e:
        print(f"[Git Push Error] {e}")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0] if keywords else "cash discount processing"
    blog = generate_blog(main_kw)

    title = blog.split("\n")[0].replace("Title:", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()

    slug = save_blog(title, content)
    update_blog_index()
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
