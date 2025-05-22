import os
import markdown2
from openai import OpenAI
from datetime import datetime
from pytrends.request import TrendReq
from git import Repo, GitCommandError, InvalidGitRepositoryError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GIT_REMOTE = os.getenv("GIT_REMOTE")

def fetch_trending_topic():
    try:
        pytrends = TrendReq()
        pytrends.build_payload(kw_list=["credit card processing"])
        trends = pytrends.related_queries()
        return next(iter(trends.values()))["top"][0]["query"]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", e)
        return "cash discount program for small businesses"

def generate_blog(topic):
    prompt = f"Write a detailed blog post for small business owners about: {topic}"
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

def format_slug(title):
    return title.lower().replace(" ", "_").replace(":", "").replace('"', '').replace("'", "").replace(",", "").replace("?", "")

def save_blog_file(title, content):
    slug = format_slug(title)
    html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>{title}</title>
</head>
<body>
<h1>{title}</h1>
<p>{content.replace("\\n", "</p><p>")}</p>
</body>
</html>"""
    path = f"frontend/blogs/{slug}.html"
    with open(path, "w") as f:
        f.write(html_content)
    return slug, path

def update_index(slug, title):
    index_path = "frontend/blog.html"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f'<div class="blog-entry"><a href="blogs/{slug}.html">{title}</a><br><small>{timestamp}</small></div>\n'
    content = ""
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            content = f.read()
    if "<!--BLOG-INSERT-->" not in content:
        content += "\n<!--BLOG-INSERT-->"
    content = content.replace("<!--BLOG-INSERT-->", entry + "<!--BLOG-INSERT-->")
    with open(index_path, "w") as f:
        f.write(content)

def git_commit_and_push(slug):
    repo_path = os.path.abspath(".")
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        repo = Repo.init(repo_path)
        origin = repo.create_remote("origin", GIT_REMOTE)
        origin.fetch()
        repo.create_head("main", origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
        print("[Git Init] Cloned and tracked origin/main")

    try:
        repo.git.add(A=True)
        repo.index.commit(f"Add blog post: {slug}")
        repo.remote(name="origin").push()
        print("[Git Push] Blog pushed to GitHub")
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")

def main():
    topic = fetch_trending_topic()
    blog = generate_blog(topic)
    lines = blog.splitlines()
    title = lines[0].replace("Title:", "").strip()
    content = "\n".join(lines[1:]).strip()
    slug, path = save_blog_file(title, content)
    print(f"Blog saved to {path}")
    update_index(slug, title)
    print("Blog index updated")
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
