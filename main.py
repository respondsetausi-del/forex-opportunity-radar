import os
import json
import requests
import feedparser
from datetime import datetime

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=forex+trading",
    "https://news.google.com/rss/search?q=prop+firm+trading",
    "https://news.google.com/rss/search?q=XAUUSD+OR+gold+trading",
    "https://news.google.com/rss/search?q=trading+journal"
]

API_KEY = os.getenv("GEMINI_API_KEY")

SHEETS_WEBHOOK = "https://script.google.com/macros/s/AKfycbzKLNWCh5d9SSrQzc2NtpjIyW_tQcm5jmuIrrH_SDD5QPDUFbSR7vALVRcUvxHht-O3/exec"

print("🚀 Forex Opportunity Radar Starting...\n")


def analyze_with_gemini(title, source, link):
    prompt = f"""
You are a Forex SaaS Opportunity Scout.

Analyze the following news headline and identify potential SaaS opportunities.

Headline:
{title}

Return ONLY valid JSON.

{{
    "date": "{datetime.now().strftime('%Y-%m-%d')}",
    "source": "{source}",
    "discussion_link": "{link}",
    "subreddit": "Google News",
    "post_title": "{title}",
    "core_problem": "",
    "pain_score": 0,
    "frequency_score": 0,
    "wtp_score": 0,
    "saas_idea": "",
    "competitors": "",
    "gap": "",
    "required_features": "",
    "recommended_stack": "",
    "apis_needed": "",
    "data_sources": "",
    "free_plan_available": "Yes/No/Partial",
    "estimated_mvp_time": "",
    "monthly_cost": "",
    "build_complexity": 0,
    "revenue_potential": 0,
    "ease_of_building": 0,
    "recommendation": "Build Now/Research Further/Ignore",
    "notes": ""
}}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=60)

        result = response.json()

        text = result["candidates"][0]["content"]["parts"][0]["text"]

        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return None


def send_to_sheets(data):
    try:
        response = requests.post(
            SHEETS_WEBHOOK,
            json=data,
            timeout=30
        )

        print(f"📤 Sent to Google Sheets: {response.status_code}")

    except Exception as e:
        print(f"❌ Sheets Error: {e}")


for feed_url in RSS_FEEDS:

    print(f"\n📡 Fetching: {feed_url}")

    feed = feedparser.parse(feed_url)

    if not feed.entries:
        print("❌ No articles found")
        continue

    print(f"✅ Found {len(feed.entries)} articles\n")

    for article in feed.entries[:5]:

        title = article.title
        link = article.link

        source = "Google News"

        print("=" * 80)
        print(f"📰 Title : {title}")
        print(f"🔗 Link  : {link}")

        analysis = analyze_with_gemini(
            title=title,
            source=source,
            link=link
        )

        if analysis:

            print("\n🤖 Gemini Analysis:")
            print(json.dumps(analysis, indent=2))

            send_to_sheets(analysis)

        print("=" * 80)

print("\n✅ Forex Opportunity Radar Completed")
