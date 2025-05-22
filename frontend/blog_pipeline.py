import os
import json
import requests
from datetime import datetime
from pytrends.request import TrendReq
from openai import OpenAI
from dotenv import load_dotenv
from git import Repo

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GIT_REPO_PATH = "./"
BLOG_FOLDER = "frontend/blogs/"
BLOG_INDEX = "frontend/blog.html"
BLUEJAY_PAT = os.getenv("BLUEJAY_PAT")
REPO_URL = "https://oauth2:" + BLUEJAY_PAT + "@github.com/mrjonwells/bluejay.git"

def fetch_trending_keywords():
    try:
        pytrends = TrendReq()
        pytrends.build_payload(["merchant services", "credit card fees", "cash discount"], timeframe="now 7-d")
        related = pytrends.related_queries()
        keywords = []
        for key in related:
            if related[key]["top"] is not None:
                for item in related[key]["top"]["query"]:
                    keywords.append(item)
        return keywords[:3]
    except Exception as e:
        print("[Fallback] Trending fetch failed:", e)
        return ["cash discount program", "merchant processing", "credit card savings"]

def generate_blog(keyword):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Write a 3-paragraph SEO blog post for small business owners about '{keyword}' focused on saving money on credit card processing fees. Include a catchy title."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content):
    safe_title = title.lower().replace(" ", "_").replace(":", "").replace("'", "")
    filename = f"{BLOG_FOLDER}{safe_title}.html"
    content_html = content.replace("\n", "</p><p>")
    with open(filename, "w") as f:
        f.write("<html><head>")
        f.write(f"<title>{title}</title>")
        f.write("</head><body>")
        f.write(f"<h2>{title}</h2>")
        f.write("<p>" + content_html + "</p>")
        f.write("</body></html>")
    print("Blog saved to", filename)
    return filename, title

def update_blog_index(filename, title):
    now = datetime.now().strftime("%B %d, %Y")
    blog_entry = f'<div class="blog-entry"><a href="{filename}">{title}</a><p>Posted {now}</p></div>\n'
    with open(BLOG_INDEX, "r") as f:
        existing = f.read()
    new_content = existing.replace("<!-- BLOG_ENTRIES -->", f"{blog_entry}<!-- BLOG_ENTRIES -->")
    with open(BLOG_INDEX, "w") as f:
        f.write(new_content)
    print("Blog index updated")

def commit_and_push():
    repo = Repo(GIT_REPO_PATH)
    repo.git.add(A=True)
    repo.index.commit("Auto-post blog from blog_pipeline")
    origin = repo.remote(name="origin")
    origin.push()
    print("Changes pushed to GitHub")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    title_line = blog.split("\n")[0]
    content = "\n".join(blog.split("\n")[1:]).strip()
    filename, title = save_blog(title_line, content)
    update_blog_index(filename, title)
    commit_and_push()

if __name__ == "__main__":
    main()
