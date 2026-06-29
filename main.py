import feedparser

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=forex+trading",
    "https://news.google.com/rss/search?q=prop+firm+trading",
    "https://news.google.com/rss/search?q=XAUUSD+OR+gold+trading",
    "https://news.google.com/rss/search?q=trading+journal"
]

print("🚀 Forex Opportunity Radar Starting...\n")

for feed_url in RSS_FEEDS:
    print(f"\n📡 Fetching: {feed_url}")

    feed = feedparser.parse(feed_url)

    if not feed.entries:
        print("❌ No articles found")
        continue

    print(f"✅ Found {len(feed.entries)} articles\n")

    for article in feed.entries[:5]:
        print("=" * 80)
        print(f"📰 Title : {article.title}")
        print(f"🔗 Link  : {article.link}")

        if hasattr(article, "published"):
            print(f"📅 Date  : {article.published}")

        print("=" * 80)