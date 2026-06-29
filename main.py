import os
import json
import requests
import feedparser

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=forex+trading",
    "https://news.google.com/rss/search?q=prop+firm+trading",
    "https://news.google.com/rss/search?q=XAUUSD+OR+gold+trading",
    "https://news.google.com/rss/search?q=trading+journal"
]

API_KEY = os.getenv("GEMINI_API_KEY")

print("🚀 Forex Opportunity Radar Starting...\n")

for feed_url in RSS_FEEDS:

    print(f"\n📡 Fetching: {feed_url}")

    feed = feedparser.parse(feed_url)

    for article in feed.entries[:3]:

        title = article.title

        prompt = f"""
You are a Forex SaaS Opportunity Scout.

Analyze this article headline and return JSON only.

Headline:
{title}

Return:

{{
  "core_problem":"",
  "pain_score":0,
  "wtp_score":0,
  "saas_idea":"",
  "recommendation":""
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

        response = requests.post(url, json=payload)

        print("\n📰", title)

        try:
            result = response.json()
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            print(text)

        except Exception as e:
            print("❌ Gemini Error:", e)
            print(response.text)
