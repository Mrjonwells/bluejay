import os
import datetime
import markdown2
from git import Repo, GitCommandError
from pytrends.request import TrendReq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BLOG_DIR = "frontend/blogs"
INDEX_FILE = "frontend/blog.html"
GIT_REMOTE = os.getenv("GIT_REMOTE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def fetch_trending_keyword():
    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload(["cash discount"], cat=0, timeframe="now 1-d", geo="US")
        related = pytrends.related_queries()
        kw = related.get("cash discount", {}).get("top", {}).get("query", [])[0]
        return kw
    except Exception:
        print("[Fallback] Trending fetch failed: list index out of range")
        return "cash discount program"

def generate_blog(keyword):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Write a helpful and persuasive blog post about '{keyword}' for small business owners interested in reducing credit card fees using cash discount programs."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700
    )
    return response.choices[0].message.content.strip()

def save_blog_file(title, content):
    slug = "_".join(title.lower().replace(":", "").replace(",", "").split())
    filename = f"{slug}.html"
    filepath = os.path.join(BLOG_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header>
    <a href="../index.html"><img src="../logo.png" alt="Logo" style="width: 120px;"></a>
  </header>
  <main>
    <h1>{title}</h1>
    {markdown2.markdown(content)}
  </main>
  <footer>
    <p>BlueJay AI Blog. Powered by AskBlueJay.ai</p>
  </footer>
</body>
</html>""")
    print(f"Blog saved to {filepath}")
    return filename

def update_blog_index():
    posts = []
    for file in sorted(os.listdir(BLOG_DIR), reverse=True):
        if file.endswith(".html"):
            path = os.path.join(BLOG_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                title = f.readline().strip().replace("<h1>", "").replace("</h1>", "")
                preview = f.readline().strip()
                posts.append((file, title, preview))

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><title>Blog</title><link rel='stylesheet' href='style.css'></head><body><h1>BlueJay Blog</h1><ul>")
        for file, title, preview in posts:
            f.write(f"<li><a href='blogs/{file}'>{title}</a><br><small>{preview}</small></li>")
        f.write("</ul></body></html>")
    print("Blog index updated")

def git_commit_and_push(slug):
    repo_path = os.getcwd()
    try:
        if not os.path.exists(os.path.join(repo_path, ".git")):
            repo = Repo.init(repo_path)
            repo.create_remote("origin", GIT_REMOTE)
        else:
            repo = Repo(repo_path)

        origin = repo.remote(name="origin")
        origin.fetch()
        repo.git.pull("origin", "main")

        repo.git.add(A=True)
        repo.index.commit(f"Add blog post: {slug}")
        origin.push()
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")
    except Exception as e:
        print(f"[Git Error] Repo setup failed: {e}")

def main():
    keyword = fetch_trending_keyword()
    blog = generate_blog(keyword)
    title = blog.split("\n")[0].replace("Title:", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()
    file_name = save_blog_file(title, content)
    update_blog_index()
    git_commit_and_push(file_name.replace(".html", ""))

if __name__ == "__main__":
    main()
