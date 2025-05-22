import os
import re
import time
import markdown2
from git import Repo, GitCommandError
from openai import OpenAI
from pytrends.request import TrendReq
from datetime import datetime

pytrends = TrendReq()

def fetch_trending_keywords():
    try:
        pytrends.build_payload(kw_list=["cash discount", "merchant services", "credit card processing"])
        related = pytrends.related_queries()
        keywords = []
        for data in related.values():
            if data and data.get("top") is not None:
                for entry in data["top"].to_dict("records"):
                    keywords.append(entry["query"])
        return keywords[:5]
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return [
            "cash discount program",
            "lower credit card fees",
            "eliminate merchant fees",
            "merchant processing AI",
            "reduce processing costs"
        ]

def generate_blog(topic):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a persuasive, informative blog post about '{topic}' for small business owners. Explain benefits, practical examples, and conclude with a strong call to action to explore cash discount programs."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def slugify(title):
    return re.sub(r'\W+', '_', title.strip().lower())

def save_blog(title, content):
    slug = slugify(title)
    filename = f"{slug}.html"
    filepath = f"frontend/blogs/{filename}"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='UTF-8'><title>{}</title></head><body>".format(title))
        f.write(f"<h2>{title}</h2>\n<p>{content.replace(chr(10), '</p><p>')}</p>")
        f.write("</body></html>")
    print(f"Blog saved to {filepath}")
    return slug

def update_blog_index(slug, title):
    index_path = "frontend/blog.html"
    with open(index_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    timestamp = datetime.now().strftime("%Y-%m-%d")
    insert_line = f'<div class="blog-entry"><a href="blogs/{slug}.html">{title}</a><p>{timestamp}</p></div>\n'

    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if "<div class=\"blog-list\">" in line and not inserted:
            new_lines.append(insert_line)
            inserted = True

    with open(index_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("Blog index updated")

def git_commit_and_push(filename):
    try:
        repo = Repo(os.getcwd())
        repo.git.add(update=True)
        repo.index.add([f"frontend/blogs/{filename}", "frontend/blog.html"])
        repo.index.commit(f"Add blog post: {filename}")

        # Ensure 'main' is checked out and tracking origin
        repo.git.checkout("main")
        repo.git.branch("--set-upstream-to=origin/main", "main")

        origin = repo.remote(name="origin")
        origin.push()
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")
    except Exception as e:
        print(f"[Git Error] {e}")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0] if keywords else "cash discount program"

    blog = generate_blog(main_kw)
    title_line = blog.splitlines()[0]
    title = title_line.replace("Title:", "").strip() if title_line.lower().startswith("title:") else main_kw.title()
    content = "\n".join(blog.split("\n")[1:]).strip()
    slug = save_blog(title, content)
    update_blog_index(slug, title)
    git_commit_and_push(f"{slug}.html")

if __name__ == "__main__":
    main()
