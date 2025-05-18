import json
import os

SEO_JSON = "backend/seo/seo_config.json"
INDEX_HTML = "frontend/index.html"

def load_seo_tags():
    with open(SEO_JSON, "r") as f:
        data = json.load(f)
        title = data.get("title", "AskBlueJay | Lower Card Fees with AI")
        description = data.get("description", "")
        keywords = data.get("keywords", [])
        keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)

        return f"""<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="keywords" content="{keywords_str}" />"""

def inject_meta_tags():
    if not os.path.exists(INDEX_HTML):
        print("index.html not found.")
        return

    with open(INDEX_HTML, "r") as f:
        content = f.read()

    new_meta = load_seo_tags()
    if "<!-- %%SEO_META_TAGS%% -->" in content:
        content = content.replace("<!-- %%SEO_META_TAGS%% -->", new_meta)
        with open(INDEX_HTML, "w") as f:
            f.write(content)
        print("SEO meta tags injected into index.html")
    else:
        print("Placeholder not found in index.html")

if __name__ == "__main__":
    inject_meta_tags()
