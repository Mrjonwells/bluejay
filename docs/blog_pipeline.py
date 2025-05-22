import os
import json
from datetime import datetime
from git import Repo, GitCommandError, InvalidGitRepositoryError
import subprocess

BLOG_FOLDER = "frontend/docs/blogs"
BLOG_INDEX = "frontend/docs/blogs/index.json"
GIT_REMOTE = os.getenv("GIT_REMOTE")

def save_blog_file(content, slug):
    os.makedirs(BLOG_FOLDER, exist_ok=True)
    file_path = os.path.join(BLOG_FOLDER, f"{slug}.html")
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Blog saved to {file_path}")
    return f"{slug}.html"

def update_blog_index(slug, topic):
    index = []
    if os.path.exists(BLOG_INDEX):
        with open(BLOG_INDEX, "r") as f:
            index = json.load(f)
    new_entry = {
        "slug": slug,
        "title": topic,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    index.insert(0, new_entry)
    with open(BLOG_INDEX, "w") as f:
        json.dump(index, f, indent=2)
    print("Blog index updated")

def git_commit_and_push(slug):
    repo_path = os.path.abspath(".")
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        print("[Git] Initializing new Git repo")
        subprocess.run(["git", "init"], cwd=repo_path)
        subprocess.run(["git", "remote", "add", "origin", GIT_REMOTE], cwd=repo_path)
        subprocess.run(["git", "config", "user.name", "BlueJay Bot"], cwd=repo_path)
        subprocess.run(["git", "config", "user.email", "bot@askbluejay.ai"], cwd=repo_path)
        subprocess.run(["git", "add", "."], cwd=repo_path)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path)
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path)
        return

    try:
        subprocess.run(["git", "config", "user.name", "BlueJay Bot"], cwd=repo_path)
        subprocess.run(["git", "config", "user.email", "bot@askbluejay.ai"], cwd=repo_path)
        subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=repo_path)
        subprocess.run(["git", "add", "."], cwd=repo_path)
        subprocess.run(["git", "commit", "-m", f"Auto-blog update: {slug}"], cwd=repo_path)
        subprocess.run(["git", "push", "origin", "main"], cwd=repo_path)
        print("[Git Push] Blog committed and pushed.")
    except GitCommandError as e:
        print("[Git Push Error]", e)

def main():
    topic = "Cash Discount Programs"
    slug = topic.lower().replace(" ", "_").replace("?", "").replace(",", "").replace("'", "")
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{topic} | AskBlueJay.ai</title>
  <meta name="description" content="Learn how {topic.lower()} can help small businesses increase profitability and reduce credit card fees.">
</head>
<body>
  <h1>{topic}</h1>
  <p>Published on {datetime.now().strftime("%B %d, %Y")}</p>
  <p>Cash discount programs are transforming the way small businesses handle credit card fees. By offering a discount to customers who pay with cash, these programs help business owners increase profitability, manage expenses, and stay competitive.</p>
  <p>Implementing a cash discount program is easy and legal in all 50 states. It also helps build stronger customer relationships and keeps more money in your pocket.</p>
  <p>Visit AskBlueJay.ai to discover how your business can save big today.</p>
</body>
</html>"""
    file_name = save_blog_file(content, slug)
    update_blog_index(slug, topic)
    git_commit_and_push(file_name.replace(".html", ""))

if __name__ == "__main__":
    main()
