import os
import re
from openai import OpenAI
from datetime import datetime
from pytrends.request import TrendReq
from git import Repo, GitCommandError, InvalidGitRepositoryError
import markdown2

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GIT_REMOTE = os.getenv("GIT_REMOTE")

def fetch_trending_topic():
    try:
        pytrends = TrendReq()
        pytrends.build_payload(["merchant services"], timeframe="now 1-d")
        return pytrends.related_queries()["merchant services"]["top"]["query"][0]
    except Exception:
        print("[Fallback] Trending fetch failed: list index out of range")
        return "cash discount program for small businesses"

def generate_blog(topic):
    prompt = f"Write an SEO-optimized blog post (title + markdown content) about: {topic}. Keep it focused on credit card processing and small business value."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def slugify(text):
    return re.sub(r'\W+', '_', text.lower()).strip('_')

def save_blog(markdown_blog):
    lines = markdown_blog.split("\n")
    title_line = lines[0].strip("# ").strip()
    content_md = "\n".join(lines[1:])
    content_html = markdown2.markdown(content_md)
    slug = slugify(title_line)
    file_name = f"{slug}.html"
    file_path = os.path.join("frontend/blogs", file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title_line}</title>
</head>
<body>
  <h1>{title_line}</h1>
  {content_html}
</body>
</html>""")
    print(f"Blog saved to {file_path}")
    return file_name

def update_index(file_name):
    blog_dir = "frontend/blogs"
    entries = []
    for file in sorted(os.listdir(blog_dir), reverse=True):
        if file.endswith(".html"):
            path = os.path.join(blog_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            title = re.search(r"<h1>(.*?)</h1>", content)
            snippet = re.search(r"<p>(.*?)</p>", content)
            if title:
                entries.append(f"<div><a href='{file}'>{title.group(1)}</a><br><small>{snippet.group(1) if snippet else ''}</small></div>")

    with open(os.path.join(blog_dir, "index.html"), "w", encoding="utf-8") as index_file:
        index_file.write("<html><body>" + "\n<hr>\n".join(entries) + "</body></html>")
    print("Blog index updated")

def git_commit_and_push(slug):
    repo_path = os.path.abspath(".")

    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        repo = Repo.init(repo_path)
        repo.create_remote("origin", GIT_REMOTE)
        print("[Git Init] Repo initialized with remote origin")

    try:
        repo.git.add(A=True)
        repo.index.commit(f"Add blog post: {slug}")
        repo.remote(name='origin').push()
        print("[Git Push] Blog pushed to GitHub")
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")

def main():
    topic = fetch_trending_topic()
    blog = generate_blog(topic)
    file_name = save_blog(blog)
    update_index(file_name)
    git_commit_and_push(file_name.replace(".html", ""))

if __name__ == "__main__":
    main()
