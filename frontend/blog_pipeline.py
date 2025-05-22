import os
import re
from openai import OpenAI
from datetime import datetime
from pytrends.request import TrendReq
import markdown2
from git import Repo, GitCommandError

# Setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pytrends = TrendReq()

# Fallback keywords
DEFAULT_KEYWORDS = [
    "cash discount program",
    "merchant processing savings",
    "credit card fees",
    "switch from Square",
    "0% processing",
    "Clover alternatives",
    "payment processing tips",
]

def fetch_trending_keywords():
    try:
        pytrends.build_payload(["merchant services"], timeframe="now 7-d")
        related = pytrends.related_queries()
        keywords = []
        for kw in related.values():
            if kw and "top" in kw:
                keywords.extend([entry["query"] for entry in kw["top"][:3]])
        if not keywords:
            raise IndexError("No keywords returned.")
        return list(set(keywords))
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return DEFAULT_KEYWORDS

def generate_blog(keyword):
    prompt = f"Write a 4-paragraph blog post for small business owners about '{keyword}', highlighting benefits, strategy, and a clear call to action."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content, slug):
    html_content = markdown2.markdown(content)
    filename = f"{slug}.html"
    path = os.path.join("frontend/blogs", filename)
    with open(path, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <header>
    <img src="../logo.png" alt="BlueJay Logo" class="centered-logo" />
    <nav class="dropdown">
      <button class="dropbtn">
        <img src="../menu-icon.png" alt="Menu" class="menu-icon" />
      </button>
      <div class="dropdown-content">
        <a href="../blog.html">Blog</a>
        <a href="https://calendly.com/askbluejay">Connect</a>
        <a href="../legal.html">Legal</a>
      </div>
    </nav>
  </header>
  <section class="hero">
    <h1>{title}</h1>
    {html_content}
  </section>
</body>
</html>""")
    print(f"Blog saved to frontend/blogs/{filename}")
    return filename

def update_blog_index(slug, title):
    index_path = "frontend/blog.html"
    with open(index_path, "r") as f:
        lines = f.readlines()

    # Find insertion point
    marker = "<!-- %%BLOG_LIST%% -->"
    now = datetime.now().strftime("%B %d, %Y")
    new_entry = f"""    <div class="blog-link">
      <a href="blogs/{slug}.html">{title}</a>
      <p class="blog-date">{now}</p>
    </div>\n"""

    for i, line in enumerate(lines):
        if marker in line:
            lines.insert(i + 1, new_entry)
            break

    with open(index_path, "w") as f:
        f.writelines(lines)

    print("Blog index updated")

def git_commit_and_push(slug):
    repo = Repo(os.getcwd())
    try:
        origin = repo.remote(name="origin")
    except ValueError:
        origin = repo.create_remote(
            "origin",
            url=f"https://{os.getenv('BLUEJAY_PAT')}@github.com/Mrjonwells/bluejay.git"
        )
    try:
        repo.git.add(A=True)
        repo.index.commit(f"Add blog: {slug}")
        origin.push()
    except GitCommandError as e:
        print(f"[Git Error] {e}")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    title = blog.split("\n")[0].replace("Title:", "").strip()
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.lower()).strip("_")
    filename = save_blog(title, "\n".join(blog.split("\n")[1:]).strip(), slug)
    update_blog_index(slug, title)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
