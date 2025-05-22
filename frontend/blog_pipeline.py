import os
import time
import requests
from pytrends.request import TrendReq
from openai import OpenAI
from datetime import datetime
import subprocess

def fetch_trending_keywords():
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload(["merchant services", "cash discount", "credit card fees"], timeframe='now 7-d')
        related = pytrends.related_queries()
        top_keywords = []
        for topic in related.values():
            if topic and topic.get("top") is not None:
                top_keywords.extend(topic["top"]["query"].tolist())
        return top_keywords[:5]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", str(e))
        return ["cash discount program"]

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    today = datetime.now().strftime("%B %d, %Y")
    prompt = f"Write a short SEO blog post (~3 paragraphs) for small business owners about '{keyword}', including stats or facts. End with a compelling call to action."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    title = content.split("\n")[0].replace("Title:", "").strip()
    slug = title.lower().replace(" ", "_").replace(":", "").replace("-", "").replace(",", "").replace(".", "")
    filename = f"frontend/blogs/{slug}.html"

    with open(filename, "w") as f:
        f.write(f"""<html>
  <head><title>{title}</title></head>
  <body>
    <h1>{title}</h1>
    <p><em>{today}</em></p>
    {"".join([f"<p>{para}</p>" for para in content.split("\\n")[1:] if para.strip()])}
  </body>
</html>""")
    print(f"Blog saved to {filename}")
    return slug, title

def update_blog_index(slug, title):
    index_file = "frontend/blog.html"
    date_str = datetime.now().strftime("%B %d, %Y")
    with open(index_file, "r") as f:
        lines = f.readlines()
    insert_idx = next(i for i, line in enumerate(lines) if "</section>" in line)
    new_entry = f'    <div class="blog-entry">\n      <a href="blogs/{slug}.html">{title}</a>\n      <p>{date_str}</p>\n    </div>\n'
    lines.insert(insert_idx, new_entry)
    with open(index_file, "w") as f:
        f.writelines(lines)
    print("Blog index updated")

def git_commit_and_push():
    token = os.getenv("BLUEJAY_PAT")
    repo_url = f"https://{token}@github.com/Mrjonwells/bluejay.git"
    os.system("git config --global user.name 'bluejay-bot'")
    os.system("git config --global user.email 'noreply@askbluejay.ai'")
    os.system("git add frontend/blogs/*.html frontend/blog.html")
    os.system(f"git commit -m 'Auto-posted blog {datetime.now().isoformat()}' || echo 'Nothing to commit'")
    os.system(f"git push {repo_url} HEAD:main")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    slug, title = generate_blog(main_kw)
    update_blog_index(slug, title)
    git_commit_and_push()

if __name__ == "__main__":
    main()
