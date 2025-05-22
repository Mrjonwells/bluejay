import os, re
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq
from dotenv import load_dotenv
from git import Repo, GitCommandError, InvalidGitRepositoryError
import markdown2

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BLUEJAY_PAT = os.getenv("BLUEJAY_PAT")
GIT_REMOTE = os.getenv("GIT_REMOTE")  # example: https://<token>@github.com/username/repo.git

def get_trending_topic():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(["cash discount"], timeframe='now 7-d')
        data = pytrends.related_queries()
        topics = list(data.values())[0]['top']['query'].tolist()
        return topics[0]
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return "cash discount program for small businesses"

def generate_blog(topic):
    prompt = f"Write a short blog post about {topic} for small business owners interested in saving money on credit card processing."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def sanitize_filename(title):
    return re.sub(r'\W+', '_', title).lower()

def save_blog_to_file(title, content):
    file_name = sanitize_filename(title) + ".html"
    full_path = os.path.join("frontend/blogs", file_name)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{title}">
</head>
<body>
  <h2>{title}</h2>
  <p>{content.replace(chr(10), '</p><p>')}</p>
</body>
</html>"""
    with open(full_path, "w") as f:
        f.write(html_content)
    print(f"Blog saved to {full_path}")
    return file_name

def update_blog_index(title, slug):
    index_path = "frontend/blog.html"
    if not os.path.exists(index_path):
        open(index_path, "w").write("<html><body><h1>Blog</h1><ul></ul></body></html>")
    with open(index_path, "r") as f:
        content = f.read()
    new_entry = f'<li><a href="blogs/{slug}.html">{title}</a> — {datetime.now().strftime("%B %d, %Y")}</li>\n'
    content = re.sub(r"(<ul>)(.*?)(</ul>)", rf"\1{new_entry}\2\3", content, flags=re.DOTALL)
    with open(index_path, "w") as f:
        f.write(content)
    print("Blog index updated")

def git_commit_and_push(slug):
    repo_path = os.path.abspath("frontend")
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        print("[Git] Initializing new Git repo")
        repo = Repo.init(repo_path)
        repo.create_remote("origin", GIT_REMOTE)

    if "origin" not in [r.name for r in repo.remotes]:
        print("[Git] Creating origin remote")
        repo.create_remote("origin", GIT_REMOTE)

    repo.git.add("--all")
    repo.index.commit(f"Add blog: {slug}")
    try:
        repo.git.pull("origin", "main", "--rebase")
    except GitCommandError as e:
        print(f"[Git Pull Error] {e}")
    try:
        repo.git.push("origin", "main")
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")

def main():
    topic = get_trending_topic()
    blog = generate_blog(topic)
    title = blog.split("\n")[0].strip().replace("Title:", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()
    file_name = save_blog_to_file(title, content)
    update_blog_index(title, file_name.replace(".html", ""))
    git_commit_and_push(file_name.replace(".html", ""))

if __name__ == "__main__":
    main()
