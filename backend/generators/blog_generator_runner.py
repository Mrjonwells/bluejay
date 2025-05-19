def update_blog_index():
    blog_dir = BLOG_OUTPUT_DIR
    blog_files = sorted(os.listdir(blog_dir), reverse=True)
    entries = []

    for file in blog_files:
        if file.endswith(".html"):
            filepath = os.path.join(blog_dir, file)
            with open(filepath, "r") as f:
                content = f.read()

            # Extract title and first sentence as summary
            title_start = content.find("<h1>") + 4
            title_end = content.find("</h1>")
            title = content[title_start:title_end].strip()

            summary_start = content.find("<div class=\"content\">") + 22
            summary_end = content.find("</div>", summary_start)
            summary = content[summary_start:summary_end].strip().replace("<br><br>", " ")[:180]

            # Extract date from filename
            date_str = file.split("-")[0:3]
            date_str = "-".join(date_str)

            entries.append((file, title, summary, date_str))

    # Build blog index
    header = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\">\n"
        "  <title>BlueJay’s Blog</title>\n"
        "  <link rel=\"stylesheet\" href=\"style.css\">\n"
        "</head>\n"
        "<body>\n"
        "<div class=\"blog-index\">\n"
        "<h1>BlueJay’s Blog</h1>\n"
        "<p>Insights on saving money, merchant processing, and modern tools for small businesses.</p>\n"
        "<ul>\n"
    )
    links = "".join([
        f"<li><a href=\"blogs/{e[0]}\">{e[1]}</a><br><em>{e[3]} – {e[2]}...</em></li>\n"
        for e in entries
    ])
    footer = "</ul>\n</div>\n</body>\n</html>"

    full_html = header + links + footer
    with open(BLOG_INDEX, "w") as f:
        f.write(full_html)
