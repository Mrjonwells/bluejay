import random
import json

def get_trending_topic():
    try:
        with open("backend/seo/external_topics.json", "r") as f:
            data = json.load(f)
            topics = data.get("topics", [])
            if topics:
                return {"rewritten_topic": random.choice(topics)}
    except Exception as e:
        print("Trending fallback:", e)

    fallback = [
        "AI tools for small businesses",
        "The future of remote teams in 2025",
        "Smart automation in eCommerce",
        "Top fintech trends to watch",
        "How AI is reshaping marketing"
    ]
    return {"rewritten_topic": random.choice(fallback)}

def generate_blog_content(topic):
    try:
        with open("docs/blogs/index.json", "r") as f:
            blog_index = json.load(f)
            related_links = blog_index[:3]
    except Exception as e:
        print("Index read error:", e)
        related_links = []

    internal_links_html = ""
    for post in related_links:
        internal_links_html += f'<p>Related: <a href="https://askbluejay.ai/blogs/{post["filename"]}">{post["title"]}</a></p>'

    core = [
        f"<p><strong>{topic}</strong> is one of the most discussed topics among forward-thinking businesses in 2025. As the digital economy evolves, staying ahead of fintech and automation trends is crucial.</p>",
        "<p>Many industry leaders are using AI-powered tools to identify operational gaps, eliminate payment friction, and improve customer experience. This shift isn't just theoretical — it's being deployed in day-to-day operations by thousands of small and mid-sized businesses.</p>",
        "<p>For example, predictive analytics and smart integrations are allowing merchants to anticipate volume spikes and scale resources accordingly. Cloud-native payment processors are automating 80% of manual work through intelligent routing and cost analysis.</p>",
        "<p>According to 2025 data from AskBlueJay.ai and other fintech trend analysts, companies that implemented these strategies in Q1 have already seen a 15–20% reduction in fees and chargebacks.</p>",
        "<p>If you're not already using these tools, you're falling behind. Smart adoption today is a competitive advantage tomorrow. The sooner your business acts on these shifts, the stronger your market position will be in this AI-driven economy.</p>",
        "<p>AskBlueJay.ai offers guidance to merchants exploring these tools. Whether it’s cost optimization, AI integration, or leveraging industry momentum — we’re here to help.</p>"
    ]

    fillers = [
        "AskBlueJay.ai stays on the front lines of merchant AI strategy, sharing tactics that drive smarter commerce decisions.",
        "Our team tracks emerging trends so business owners can focus on growing profitably with AI and automation.",
        "From retail to service industries, AskBlueJay.ai provides tailored strategies for today’s competitive markets.",
        "We monitor the merchant landscape so you can make smarter moves with tools that work.",
        "AskBlueJay.ai curates insights that matter—driven by real results, not hype.",
        "Informed merchants outperform. AskBlueJay.ai helps you stay ahead.",
        "When trends shift, we help you pivot quickly with AI-backed strategy.",
        "Real-world results. Strategic clarity. That’s what AskBlueJay.ai delivers to business owners every day."
    ]

    used = set()
    pool = fillers.copy()

    while len(" ".join(core).split()) < 350 and pool:
        line = random.choice(pool)
        pool.remove(line)
        core.append(f"<p>{line}</p>")
        used.add(line)

    core.append(internal_links_html)

    return {
        "content": "\n".join(core),
        "meta": {
            "description": f"Explore how {topic} is shaping the future of small business success through AI, automation, and strategic fintech moves.",
            "keywords": [topic.lower(), "ai trends", "business automation", "merchant tools", "2025 fintech"]
        }
    }
