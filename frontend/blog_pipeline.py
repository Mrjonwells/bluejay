import os
import time
import markdown2
from git import Repo, GitCommandError
from pytrends.request import TrendReq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BLOG_DIR = "frontend/blogs/"
INDEX_FILE = "frontend/blog.html"
REPO_DIR = os.getcwd()
GIT_TOKEN = os.getenv("BLUEJAY_PAT")
REPO_URL = f"https://{GIT_TOKEN}@github.com/Mrjonwells/bluejay.git"

def fetch_trending_keywords():
    pytrends = TrendReq()
    try:
        pytrends.build_payload(["merchant processing"])
        related = pytrends.related_queries()
        kw_list = list(related.values())[0]["top"]
        return [kw["query"] for kw in kw_list if "query" in kw]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", str(e))
        return ["cash discount program", "merchant services", "credit card processing"]

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a helpful SEO-optimized blog post about '{keyword}' for small business owners interested in saving money on credit card processing. Include a hook, value, and call to action."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    blog = response.choices[0].message.content.strip()
    title = blog.split("\n")[0].replace("Title: ", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()
    return title, content

def save_blog(title, content, slug):
    filename = f"{BLOG_DIR}{slug}.html"
    os.makedirs(BLOG_DIR, exist_ok=True)
    formatted_content = content.replace("\n", "</p><p>")
    with open(filename, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{title}</title></head>
<body>
<h2>{title}</h2>
<p>{formatted_content}</p>
</body>
</html>""")
    print(f"Blog saved to {filename}")

def update_blog_index(title, slug):
    entry = f'<div class="blog-entry"><a href="blogs/{slug}.html">{title}</a></div>\n'
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "w") as f:
            f.write("<html><body>\n")
    with open(INDEX_FILE, "r+") as f:
        lines = f.readlines()
        if entry not in lines:
            f.seek(0, 0)
            f.write(entry + "".join(lines))
    print("Blog index updated")

def slugify(title):
    return title.lower().replace(" ", "_").replace(":", "").replace("-", "_").replace("__", "_")

def git_commit_and_push(slug):
    repo = Repo(REPO_DIR)
    try:
        repo.git.fetch()
        repo.git.checkout("main")
        repo.git.pull("origin", "main")
        repo.git.branch("--set-upstream-to=origin/main", "main")
    except GitCommandError as e:
        print("[Git Error] during setup:", e)

    repo.git.add("--all")
    repo.index.commit(f"Add blog post: {slug}")
    try:
        repo.remote(name='origin').push()
        print("Blog successfully pushed to GitHub.")
    except GitCommandError as e:
        print("[Git Push Error]", e)

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    title, content = generate_blog(main_kw)
    slug = slugify(title)
    save_blog(title, content, slug)
    update_blog_index(title, slug)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
