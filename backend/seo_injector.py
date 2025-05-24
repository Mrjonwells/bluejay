import os

SEO_HTML = "backend/seo/seo_injection.html"
INDEX_HTML = "docs/index.html"
PLACEHOLDER = "<!-- %%SEO_META_TAGS%% -->"

def inject_seo():
    if not os.path.exists(SEO_HTML):
        print("SEO injection HTML not found.")
        return

    if not os.path.exists(INDEX_HTML):
        print("index.html not found.")
        return

    with open(SEO_HTML, "r") as f:
        seo_tags = f.read()

    with open(INDEX_HTML, "r") as f:
        content = f.read()

    if PLACEHOLDER not in content:
        print("Placeholder not found in index.html. No changes made.")
        return

    updated = content.replace(PLACEHOLDER, seo_tags)

    with open(INDEX_HTML, "w") as f:
        f.write(updated)

    print("SEO meta tags successfully injected.")

if __name__ == "__main__":
    inject_seo()
