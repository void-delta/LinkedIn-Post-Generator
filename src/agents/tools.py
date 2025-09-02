from typing import List, Dict
import requests
from src.config import settings

NEWS_URL = "https://newsapi.org/v2/everything"


def get_recent_news(query: str, limit: int = 3) -> List[Dict]:
    """
    Fetch recent news articles related to the query using NewsAPI.
    Requires NEWS_API_KEY in environment.

    Returns: list of dicts with keys: title, url, desc, source
    """
    if not settings.news_api_key:
        return []

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": settings.news_api_key,
        "pageSize": limit,
    }

    try:
        res = requests.get(NEWS_URL, params=params, timeout=10)
        data = res.json()

        articles = data.get("articles", [])[:limit]
        return [
            {
                "title": a.get("title"),
                "url": a.get("url"),
                "desc": a.get("description", ""),
                "source": (a.get("source") or {}).get("name", ""),
            }
            for a in articles
        ]
    except Exception:
        return []
