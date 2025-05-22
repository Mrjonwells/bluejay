import os
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq
from git import Repo, GitCommandError
from dotenv import load_dotenv

load_dotenv()

SEO_TOPICS = [
    "cash discount program", "credit card processing", "small business fees",
    "merchant processing", "save on transaction fees", "dual pricing strategy"
]

REPO_URL = "https://github.com/Mrjonwells/bluejay.git"
BLOG_DIR = "frontend/blogs"
BLOG_INDEX = "frontend/blog.html"

def fetch_trending_keywords():
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload(["merchant services"], cat=0, timeframe='now 7-d', geo='US', gprop='')
        related = pytrends.related_queries()
        trends = related['merchant services']['top']
        return [row['query'] for row in trends.head(5).to_dict('records')] if trends is not None else []
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return SEO_TOPICS

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Write a blog post for small business owners about '{keyword}' in the context of saving money using cash discount programs. Make it persuasive, simple, and actionable."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content, filename):
    with open(os.path.join(BLOG_DIR, filename), "w") as f:
        f.write("<html><head>")
        f.write(f"<title>{title}</title>")
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        f.write("</head><body style='background-color:#0d0d0d;color:#eaeaea;font-family:sans-serif;padding:20px;'>")
        f.write(f"<h2>{title}</h2>")
        f.write("<p>" + content.replace("\n", "</p><p>") + "</p>")
        f.write("</body></html>")
    print(f"Blog saved to {os.path.join(BLOG_DIR, filename)}")

def update_index(title, filename):
    with open(BLOG_INDEX, "r") as f:
        lines = f.readlines()

    insert_index = next(i for i, line in enumerate(lines) if "</main>" in line)
    summary = f"{title.split(':')[0]} — Learn how small businesses can save on fees."
    date = datetime.now().strftime("%Y-%m-%d")
    entry = f'  <div class="blog-preview"><a href="blogs/{filename}">{title}</a><br/><small>{date}</small><p>{summary}</p></div>\n'

    lines.insert(insert_index, entry)

    with open(BLOG_INDEX, "w") as f:
        f.writelines(lines)
    print("Blog index updated")

def git_commit_and_push(slug):
    repo = Repo(os.getcwd())
    try:
        origin = repo.remote(name="origin")
    except ValueError:
        origin = repo.create_remote("origin", url=REPO_URL)

    try:
        repo.git.checkout("main")
    except GitCommandError as e:
        print(f"[Git Checkout Error] {e}")

    try:
        repo.git.add(A=True)
        repo.index.commit(f"Add blog: {slug}")
        try:
            origin.push(refspec="main:main", set_upstream=True)
        except GitCommandError:
            repo.git.push("--set-upstream", "origin", "main")
    except GitCommandError as e:
        print(f"[Git Push Error] {e}")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0] if keywords else "cash discounting"
    blog = generate_blog(main_kw)
    title = blog.split("\n")[0].replace("Title: ", "").strip()
    content = "\n".join(blog.split("\n")[1:]).strip()
    slug = title.lower().replace(" ", "_").replace(":", "").replace(",", "")
    filename = f"{slug}.html"

    save_blog(title, content, filename)
    update_index(title, filename)
    git_commit_and_push(slug)

if __name__ == "__main__":
    main()
