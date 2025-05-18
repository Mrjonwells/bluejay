import json
import os

SEO_JSON = "backend/seo/seo_config.json"
INDEX_HTML = "frontend/index.html"
PLACEHOLDER = "<!-- %%SEO_META_TAGS%% -->"

def load_seo_tags():
    with open(SEO_JSON, "r") as f:
        data = json.load(f)
        title = data.get("title", "")
        description = data.get("description", "")
        keywords = ", ".join(data.get("keywords", []))
        return f"""<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="keywords" content="{keywords}" />"""

def inject_meta_tags():
    if not os.path.exists(INDEX_HTML):
        print("index.html not found.")
        return

    with open(INDEX_HTML, "r") as f:
        content = f.read()

    if PLACEHOLDER not in content:
        print("Placeholder not found in index.html")
        return

    new_meta = load_seo_tags()
    updated = content.replace(PLACEHOLDER, new_meta)

    with open(INDEX_HTML, "w") as f:
        f.write(updated)

    print("SEO meta tags injected into index.html")

if __name__ == "__main__":
    inject_meta_tags()
