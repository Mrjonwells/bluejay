import json
import os

# Paths
SEO_CONFIG_PATH = "backend/seo/seo_config.json"
INJECTION_HTML_PATH = "backend/seo/seo_injection.html"
INDEX_HTML_PATH = "frontend/index.html"

def generate_seo_injection():
    with open(SEO_CONFIG_PATH, "r") as f:
        config = json.load(f)

    title = config.get("title", "")
    description = config.get("meta_description", "")
    keywords = ", ".join(config.get("keywords", []))
    structured_data = json.dumps(config.get("structured_data", {}), indent=2)

    html = f"""<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="keywords" content="{keywords}" />
<script type="application/ld+json">
{structured_data}
</script>"""

    with open(INJECTION_HTML_PATH, "w") as f:
        f.write(html.strip())

    print("SEO injection HTML updated.")

def inject_into_index():
    with open(INJECTION_HTML_PATH, "r") as inject:
        injection = inject.read()

    with open(INDEX_HTML_PATH, "r") as index:
        content = index.read()

    pre = "<!-- SEO-INJECT-START -->"
    post = "<!-- SEO-INJECT-END -->"
    if pre in content and post in content:
        start = content.index(pre) + len(pre)
        end = content.index(post)
        new_content = content[:start] + "\n" + injection + "\n" + content[end:]
        with open(INDEX_HTML_PATH, "w") as index:
            index.write(new_content)
        print("index.html SEO block updated.")
    else:
        print("Injection tags not found in index.html.")

if __name__ == "__main__":
    generate_seo_injection()
    inject_into_index()
