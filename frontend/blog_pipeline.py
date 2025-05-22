import os
import re
import markdown2
from git import Repo, GitCommandError
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq

# Setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GIT_TOKEN = os.getenv("BLUEJAY_PAT")
REPO_URL = f"https://{GIT_TOKEN}@github.com/Mrjonwells/bluejay.git"
BLOG_DIR = "frontend/blogs/"
INDEX_FILE = "frontend/blog.html"

client = OpenAI(api_key=OPENAI_API_KEY)
pytrends = TrendReq(hl="en-US", tz=360)


def fetch_trending_keywords():
    try:
        pytrends.build_payload(["credit card processing"], cat=0, timeframe="now 7-d", geo="", gprop="")
        related = pytrends.related_queries()
        top_keywords = related.get("credit card processing", {}).get("top", {}).get("query", [])
        return [k for k in top_keywords if isinstance(k, str)]
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return [
            "cash discount program",
            "merchant processing fees",
            "credit card surcharges",
            "small business payment solutions",
            "card processing savings"
        ]


def generate_blog(topic):
    system_prompt = (
        "You are a professional blog writer for AskBlueJay.ai, focused on helping small businesses save money on "
        "credit card fees using cash discount programs and advanced merchant processing strategies. Write in a clean, "
        "clear tone that resonates with small business owners. Include a compelling title and intro."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write a blog post about: {topic}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


def save_blog_to_file(title, content):
    slug = re.sub(r"[^\w]+", "_", title.lower()).strip("_")
    filename = os.path.join(BLOG_DIR, f"{slug}.html")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n")
        f.write(f"<meta charset=\"UTF-8\">\n<title>{title}</title>\n")
        f.write("<link rel=\"stylesheet\" href=\"../style.css\">\n</head>\n<body>\n")
        f.write(f"<article class='blog-post'>\n<h1>{title}</h1>\n")
        f.write(f"{markdown2.markdown(content)}")
        f.write("\n</article>\n</body>\n</html>")

    print(f"Blog saved to {filename}")
    return slug


def update_blog_index(title, slug):
    post_url = f"blogs/{slug}.html"
    today = datetime.now().strftime("%B %d, %Y")
    entry = f'<div class="blog-preview"><a href="{post_url}">{title}</a><p>{today}</p></div>\n'

    with open(INDEX_FILE, "r+", encoding="utf-8") as index_file:
        content = index_file.read()
        updated = re.sub(r"(<!-- BLOG_ENTRIES_START -->)", rf"\1\n{entry}", content)
        index_file.seek(0)
        index_file.write(updated)
        index_file.truncate()

    print("Blog index updated")


def git_commit_and_push(slug):
    repo = Repo(os.getcwd())
    try:
        origin = repo.remote(name="origin")
    except ValueError:
        origin = repo.create_remote("origin", url=REPO_URL)

    if repo.head.is_detached:
        repo.git.checkout("-B", "main")

    try:
        repo.git.add(A=True)
        repo.index.commit(f"Add blog: {slug}")
        repo.git.push("--set-upstream", "origin", "main")
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")


def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0] if keywords else "cash discount program"
    blog = generate_blog(main_kw)

    title = blog.split("\n")[0].replace("Title: ", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()

    slug = save_blog_to_file(title, content)
    update_blog_index(title, slug)
    git_commit_and_push(slug)


if __name__ == "__main__":
    main()
