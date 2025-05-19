def update_blog_index(new_entry):
    entries = []
    if os.path.exists(BLOG_INDEX):
        with open(BLOG_INDEX, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith("<li><a href=\"blogs/"):
                    parts = line.strip().split(">")
                    link = parts[1].split("<")[0].split("/")[-1]
                    title = parts[2].split("<")[0]
                    date_line = next((l for l in lines if f">{title}</a><br>" in l), "")
                    date = date_line.split("–")[0].split("</em>")[0].strip().split()[-1]
                    summary = date_line.split("–")[-1].split("...")[0].strip()
                    entries.append((link, title, summary, date))

    # Avoid duplication
    entries = [e for e in entries if e[0] != new_entry[0]]
    entries.insert(0, new_entry)

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
        f"<li><a href=\"blogs/{e[0]}\">{e[1]}</a><br><em>{e[3]} – {e[2][:180].strip()}...</em></li>\n"
        for e in entries
    ])
    footer = "</ul>\n</div>\n</body>\n</html>"

    with open(BLOG_INDEX, "w") as f:
        f.write(header + links + footer)