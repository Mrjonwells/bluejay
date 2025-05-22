import os
import re
import markdown2
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq
from git import Repo

BLOG_FOLDER = "frontend/blogs/"
BLOG_INDEX = "frontend/blog.html"

def fetch_trending_keywords():
    pytrends = TrendReq()
    try:
        pytrends.build_payload(["cash discount", "merchant services"], timeframe="now 7-d")
        related = pytrends.related_queries()
        suggestions = []
        for kw_data in related.values():
            try:
                for item in kw_data['top']['query']:
                    suggestions.append(item)
            except Exception:
                continue
        return suggestions if suggestions else []
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return []

def generate_blog(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a blog post for small business owners about: {topic}. Focus on practical merchant services advice and cash discounting."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_blog(title, body):
    slug = re.sub(r'\W+', '_', title.lower()).strip("_")
    filename = f"{slug}.html"
    filepath = os.path.join(BLOG_FOLDER, filename)
    content = "\n".join(body.split("\n")[1:]).strip()

    with open(filepath, "w", encoding="utf-8") as f:
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
    <a href="../index.html"><img src="../logo.png" alt="BlueJay Logo" class="centered-logo" /></a>
  </header>
  <main class="blog-post">
    <h1>{title}</h1>
    <p><em>{datetime.now().strftime("%B %d, %Y")}</em></p>
    <p>{content.replace(chr(10), '</p><p>')}</p>
  </main>
</body>
</html>""")
    return slug, title, content

def update_blog_index(slug, title, summary):
    try:
        with open(BLOG_INDEX, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["<!DOCTYPE html>\n<html>\n<head>\n<title>Blog</title>\n</head>\n<body>\n<h1>BlueJay Blog</h1>\n<ul>\n"]

    # Remove previous entry with same slug
    lines = [line for line in lines if slug not in line]

    new_entry = f'<li><a href="blogs/{slug}.html">{title}</a><br><small>{summary[:140]}...</small></li>\n'

    if "</ul>" not in lines:
        lines.append("<ul>\n")
        lines.append(new_entry)
        lines.append("</ul>\n</body>\n</html>")
    else:
        index = lines.index("</ul>\n")
        lines.insert(index, new_entry)

    with open(BLOG_INDEX, "w", encoding="utf-8") as f:
        f.writelines(lines)

def git_commit_and_push(slug):
    repo = Repo(os.getcwd())
    if 'origin' not in [r.name for r in repo.remotes]:
        repo.create_remote('origin', 'https://github.com/Mrjonwells/bluejay.git')
    repo.git.add(A=True)
    repo.index.commit(f"Add new blog post: {slug}")
    repo.remote(name='origin').push(env={
        'GIT_ASKPASS': 'echo',
        'GIT_USERNAME': 'BlueJay',
        'GIT_TOKEN': os.getenv("BLUEJAY_PAT")
    })

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0] if keywords else "Cash Discount Programs for Small Businesses"
    blog = generate_blog(main_kw)
    title = blog.split("\n")[0].replace("Title:", "").strip()
    slug, clean_title, content = save_blog(title, blog)
    update_blog_index(slug, clean_title, content)
    print(f"Blog saved to {BLOG_FOLDER}{slug}.html")
    print("Blog index updated")
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
