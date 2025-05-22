import os
import re
import markdown2
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq
from git import Repo, GitCommandError

GIT_REMOTE = os.getenv("GIT_REMOTE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_trending_keyword():
    try:
        pytrends = TrendReq()
        pytrends.build_payload(["merchant processing"], timeframe="now 1-d")
        trends = pytrends.related_queries()
        kw = next(iter(trends))
        return trends[kw]["top"]["query"][0]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", str(e))
        return "cash discount program for small businesses"

def generate_blog(topic):
    prompt = f"""Write an SEO-optimized blog post for small business owners about: "{topic}". 
Make it informative, persuasive, and 3-5 paragraphs long. Include a clear title and strong call to action."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

def save_blog(title, body):
    slug = re.sub(r"[^\w]+", "_", title.lower()).strip("_")
    filename = f"{slug}.html"
    full_path = os.path.join("frontend/blogs", filename)

    body_html = markdown2.markdown(body)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header><a href="../blog.html" class="back-link">← Back to Blog Index</a></header>
  <main class="blog-post">
    <h1>{title}</h1>
    {body_html}
  </main>
</body>
</html>""")
    print(f"Blog saved to {full_path}")
    return filename

def update_index():
    blog_dir = "frontend/blogs"
    posts = sorted([f for f in os.listdir(blog_dir) if f.endswith(".html")])
    index_path = "frontend/blog.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>BlueJay Blog</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header><a href="index.html" class="back-link">← Back to Home</a></header>
  <main class="blog-index">
    <h1>BlueJay Blog</h1>
""")
        for post in posts:
            title = post.replace("_", " ").replace(".html", "").title()
            f.write(f'<div class="blog-preview"><a href="blogs/{post}">{title}</a></div>\n')
        f.write("</main></body></html>")
    print("Blog index updated")

def git_commit_and_push(slug):
    repo_path = os.getcwd()
    try:
        if not os.path.exists(os.path.join(repo_path, ".git")):
            repo = Repo.init(repo_path)
            if "origin" not in [r.name for r in repo.remotes]:
                repo.create_remote("origin", GIT_REMOTE)
        else:
            repo = Repo(repo_path)

        origin = [r for r in repo.remotes if r.name == "origin"]
        if not origin:
            raise Exception("Remote 'origin' was not found.")
        origin = origin[0]

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
    topic = fetch_trending_keyword()
    blog = generate_blog(topic)
    title = blog.splitlines()[0].replace("Title:", "").strip()
    content = "\n".join(blog.splitlines()[1:]).strip()
    file_name = save_blog(title, content)
    update_index()
    git_commit_and_push(file_name.replace(".html", ""))

if __name__ == "__main__":
    main()
