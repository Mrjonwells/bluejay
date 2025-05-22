import os
import time
import markdown2
import subprocess
from git import Repo
from pytrends.request import TrendReq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

REPO_URL = "https://github.com/Mrjonwells/bluejay.git"
LOCAL_REPO_PATH = "/tmp/bluejay"
BLOG_FOLDER = os.path.join(LOCAL_REPO_PATH, "frontend", "blogs")
INDEX_FILE = os.path.join(LOCAL_REPO_PATH, "frontend", "blog.html")

def fetch_trending_keywords():
    try:
        pytrends = TrendReq()
        pytrends.build_payload(["cash discount", "merchant services"], timeframe="now 7-d")
        related = pytrends.related_queries()
        kw_list = list(related.values())[0]['top']
        return [x['query'] for x in kw_list[:5]]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", e)
        return [
            "cash discount program",
            "merchant processing fees",
            "save on credit card fees",
            "small business payments",
            "credit card processing AI"
        ]

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a blog writer for small businesses focused on payments and savings."},
            {"role": "user", "content": f"Write a blog post about '{keyword}' that explains its benefits to small business owners in 3-4 paragraphs with a helpful tone. Include a catchy title."}
        ]
    )
    return response.choices[0].message.content

def save_blog_file(slug, html):
    filename = os.path.join(BLOG_FOLDER, f"{slug}.html")
    with open(filename, "w") as f:
        f.write(html)
    print("Blog saved to", filename)

def update_blog_index(slug, title, preview):
    with open(INDEX_FILE, "r") as f:
        lines = f.readlines()
    new_entry = f'<div class="blog-entry"><a href="blogs/{slug}.html">{title}</a><p>{preview}</p></div>\n'
    insert_at = next((i for i, line in enumerate(lines) if "<!-- BLOG_ENTRIES -->" in line), -1)
    if insert_at != -1:
        lines.insert(insert_at + 1, new_entry)
        with open(INDEX_FILE, "w") as f:
            f.writelines(lines)
        print("Blog index updated")

def git_commit_and_push(slug):
    git_env = {
        "GIT_AUTHOR_NAME": "bluejay",
        "GIT_AUTHOR_EMAIL": "bot@askbluejay.ai",
        "GIT_COMMITTER_NAME": "bluejay",
        "GIT_COMMITTER_EMAIL": "bot@askbluejay.ai",
        "GIT_ASKPASS": "echo",
        "BLUEJAY_PAT": os.getenv("BLUEJAY_PAT")
    }
    if os.path.exists(LOCAL_REPO_PATH):
        subprocess.run(["rm", "-rf", LOCAL_REPO_PATH], check=True)
    Repo.clone_from(REPO_URL.replace("https://", f"https://{git_env['BLUEJAY_PAT']}@"), LOCAL_REPO_PATH, env=git_env)
    subprocess.run(["git", "checkout", "-B", "main"], cwd=LOCAL_REPO_PATH, check=True)
    subprocess.run(["git", "branch", "--set-upstream-to=origin/main", "main"], cwd=LOCAL_REPO_PATH, check=True)

    subprocess.run(["git", "add", "."], cwd=LOCAL_REPO_PATH, check=True)
    subprocess.run(["git", "commit", "-m", f"Add blog: {slug}"], cwd=LOCAL_REPO_PATH, check=True)
    try:
        subprocess.run(["git", "push"], cwd=LOCAL_REPO_PATH, check=True)
    except subprocess.CalledProcessError as e:
        print("[Git Push Error]", e)

def main():
    keywords = fetch_trending_keywords()
    for kw in keywords:
        blog = generate_blog(kw)
        lines = blog.split("\n")
        title = lines[0].replace("Title: ", "").strip().strip('"')
        content = "\n".join(lines[1:]).strip()
        slug = title.lower().replace(" ", "_").replace(":", "").replace(",", "").replace(".", "")
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="blog-post">
    <h1>{title}</h1>
    <p>{content.replace("\n", "</p><p>")}</p>
  </div>
</body>
</html>"""
        save_blog_file(slug, html)
        update_blog_index(slug, title, content[:160] + "...")
        git_commit_and_push(slug)
        break

if __name__ == "__main__":
    main()
