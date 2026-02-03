import os
from datetime import datetime

import requests
from django.shortcuts import render

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"

CATEGORIES = [
    {"slug": "general", "label": "Top Stories", "icon": "🗞️"},
    {"slug": "technology", "label": "Technology", "icon": "💻"},
    {"slug": "sports", "label": "Sports", "icon": "🏅"},
    {"slug": "business", "label": "Business", "icon": "📈"},
    {"slug": "entertainment", "label": "Entertainment", "icon": "🎬"},
    {"slug": "science", "label": "Science", "icon": "🔬"},
    {"slug": "health", "label": "Health", "icon": "🧠"},
]

COUNTRIES = {
    "us": "United States",
    "gb": "United Kingdom",
    "ca": "Canada",
    "au": "Australia",
    "in": "India",
}


def fetch_news(category, country, query):
    """Fetch news articles from News API with optional category and search."""
    if not NEWS_API_KEY:
        return [], "Missing NEWS_API_KEY environment variable. Add it to fetch live news."

    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": 20,
    }

    if category and category != "general":
        params["category"] = category

    if query:
        params["q"] = query

    response = requests.get(TOP_HEADLINES_URL, params=params, timeout=10)
    if response.status_code == 200:
        payload = response.json()
        return payload.get("articles", []), None

    return [], "News service is temporarily unavailable. Please try again later."


def normalize_articles(articles):
    """Normalize article fields for display-friendly templates."""
    normalized = []
    for article in articles:
        published_at = article.get("publishedAt")
        formatted_date = None
        if published_at:
            try:
                formatted_date = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            except ValueError:
                formatted_date = None

        normalized.append(
            {
                "title": article.get("title") or "Untitled story",
                "description": article.get("description") or "No description available.",
                "url": article.get("url"),
                "image": article.get("urlToImage"),
                "source": (article.get("source") or {}).get("name", "Unknown source"),
                "author": article.get("author") or "Staff Reporter",
                "published": formatted_date,
            }
        )
    return normalized


def home(request):
    category = request.GET.get("category", "general")
    country = request.GET.get("country", "us")
    query = request.GET.get("q", "").strip()

    if category not in {item["slug"] for item in CATEGORIES}:
        category = "general"

    if country not in COUNTRIES:
        country = "us"

    articles, error_message = fetch_news(category, country, query)
    headlines = normalize_articles(articles)

    hero_story = headlines[0] if headlines else None
    secondary_stories = headlines[1:5]
    latest_stories = headlines[5:]

    context = {
        "hero_story": hero_story,
        "secondary_stories": secondary_stories,
        "latest_stories": latest_stories,
        "categories": CATEGORIES,
        "countries": COUNTRIES,
        "active_category": category,
        "active_country": country,
        "active_country_label": COUNTRIES.get(country, "Global"),
        "query": query,
        "error_message": error_message,
        "total_results": len(headlines),
    }
    return render(request, "news_app/home.html", context)
