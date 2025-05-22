import os
from openai import OpenAI
from datetime import datetime
from pytrends.request import TrendReq

def fetch_trending_keywords():
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload(["credit card processing"], cat=0, timeframe='now 1-d', geo='US', gprop='')
        related = pytrends.related_queries()
        ranked = related["credit card processing"]["top"]
        if ranked is None or ranked.empty:
            raise IndexError("Trending fetch failed")
        return [kw for kw in ranked['query'].tolist() if "card" in kw.lower() or "merchant" in kw.lower()]
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return ["cash discount", "credit card surcharges", "merchant fees"]

def generate_blog(keyword):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Write a helpful 5-paragraph blog post for small business owners about "{keyword}" as it relates to saving money on credit card processing fees. Start with a compelling title, and close with a strategic call to action."""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def sanitize_filename(title):
    return ''.join(c if c.isalnum() or c in ('_', '-') else '_' for c in title.lower().replace(' ', '_')) + ".html"

def save_blog(title, content):
    folder = "frontend/blogs"
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(title)
    filepath = os.path.join(folder, filename)

    content = "\n".join(content.split("\n")[1:]).strip()  # strip title line
    with open(filepath, "w") as f:
        f.write(f"""<html>
<head><title>{title}</title></head>
<body>
<h2>{title}</h2>
<p>{content.replace(chr(10), '</p><p>')}</p>
</body>
</html>""")
    
    print(f"Blog saved to {filepath}")
    return filename, title, content[:180]

def update_index(entry_list):
    index_path = "frontend/blog.html"
    with open(index_path, "w") as f:
        f.write("<html><head><title>BlueJay Blog</title></head><body>")
        f.write("<h1>BlueJay’s Blog</h1><ul>")
        for filename, title, summary in entry_list:
            f.write(f'<li><a href="blogs/{filename}">{title}</a><br><small>{summary}...</small></li><br>')
        f.write("</ul></body></html>")
    print("Blog index updated")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    title = blog.split("\n")[0].replace("Title:", "").strip()
    filename, title, summary = save_blog(title, blog)
    update_index([(filename, title, summary)])

if __name__ == "__main__":
    main()
