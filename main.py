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

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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


def send_to_telegram(data):
    message = f"""
🚨 NEW FOREX SaaS OPPORTUNITY

💡 Idea
{data.get('saas_idea','')}

🔥 Pain
{data.get('pain_score',0)}/10

📈 Frequency
{data.get('frequency_score',0)}/10

💰 Willingness To Pay
{data.get('wtp_score',0)}/10

🧩 Core Problem
{data.get('core_problem','')}

🏆 Recommendation
{data.get('recommendation','')}

📰 Headline
{data.get('post_title','')}

🔗
{data.get('discussion_link','')}
"""

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=30
        )

        print(f"📲 Telegram: {response.status_code}")

    except Exception as e:
        print(f"❌ Telegram Error: {e}")


def send_to_sheets(data):
    try:
        response = requests.post(
            SHEETS_WEBHOOK,
            json=data,
            timeout=30
        )

        print(f"📤 Google Sheets: {response.status_code}")

    except Exception as e:
        print(f"❌ Sheets Error: {e}")


for feed_url in RSS_FEEDS:

    print(f"\n📡 Fetching: {feed_url}")

    feed = feedparser.parse(feed_url)

    if not feed.entries:
        print("❌ No articles found")
        continue

    print(f"✅ Found {len(feed.entries)} articles")

    for article in feed.entries[:5]:

        title = article.title
        link = article.link
        source = "Google News"

        print("=" * 80)
        print(title)

        analysis = analyze_with_gemini(
            title=title,
            source=source,
            link=link
        )

        if analysis:

            print(json.dumps(analysis, indent=2))

            send_to_telegram(analysis)

            send_to_sheets(analysis)

        print("=" * 80)

print("\n✅ Forex Opportunity Radar Completed")
