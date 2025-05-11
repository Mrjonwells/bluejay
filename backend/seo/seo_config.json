import json
import os
from datetime import datetime

SEO_CONFIG_PATH = "backend/seo/seo_config.json"
INDEX_HTML_PATH = "index.html"

def generate_meta_tags(config):
    meta = []
    meta.append(f'<meta name="description" content="{config.get("description", "")}" />')
    meta.append(f'<meta name="keywords" content="{", ".join(config.get("keywords", []))}" />')
    meta.append('<script type="application/ld+json">')
    meta.append(json.dumps(config.get("schema", {}), indent=2))
    meta.append('</script>')
    return "\n  ".join(meta)

def inject_seo():
    if not os.path.exists(SEO_CONFIG_PATH):
        print(f"[{datetime.utcnow()}] SEO config file not found.")
        return

    with open(SEO_CONFIG_PATH, "r") as f:
        config = json.load(f)

    meta_block = generate_meta_tags(config)

    if not os.path.exists(INDEX_HTML_PATH):
        print(f"[{datetime.utcnow()}] index.html not found.")
        return

    with open(INDEX_HTML_PATH, "r") as f:
        index_html = f.read()

    if "<!-- %%SEO_META_TAGS%% -->" not in index_html:
        print(f"[{datetime.utcnow()}] SEO injection placeholder not found in index.html.")
        return

    updated_html = index_html.replace("<!-- %%SEO_META_TAGS%% -->", meta_block)

    with open(INDEX_HTML_PATH, "w") as f:
        f.write(updated_html)

    print(f"[{datetime.utcnow()}] SEO tags injected into index.html successfully.")

if __name__ == "__main__":
    inject_seo()
