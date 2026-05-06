import httpx
import logging
from typing import List, Optional
from datetime import datetime
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class NewsService:
    """Service for fetching news from external APIs"""
    
    def __init__(self):
        self.dev_to_base_url = "https://dev.to/api/articles"
        self.newsapi_base_url = "https://newsapi.org/v2"
        self.hn_base_url = "https://hacker-news.firebaseio.com/v0"
        self.timeout = 10.0
    
    async def fetch_devto_articles(self, limit: int = 30) -> List[dict]:
        """Fetch latest articles from Dev.to"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.dev_to_base_url,
                    params={
                        "per_page": limit,
                        "state": "published"
                    },
                    headers={"api-key": settings.dev_to_api_key} if settings.dev_to_api_key else {}
                )
                response.raise_for_status()
                articles = response.json()
                
                # Transform Dev.to format to our format
                return [
                    {
                        "title": article.get("title"),
                        "description": article.get("description", ""),
                        "content": article.get("body_markdown", ""),
                        "url": article.get("url"),
                        "source": "devto",
                        "source_id": str(article.get("id")),
                        "author": article.get("user", {}).get("name"),
                        "published_at": article.get("published_at"),
                        "upvotes": article.get("positive_reactions_count", 0),
                        "comments": article.get("comments_count", 0),
                        "tags": ",".join(article.get("tags", [])),
                        "category": article.get("tags", ["general"])[0] if article.get("tags") else "general"
                    }
                    for article in articles
                ]
        except httpx.HTTPError as e:
            logger.error(f"Dev.to API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching Dev.to: {e}")
            return []
    
    async def fetch_hackernews_articles(self, limit: int = 30) -> List[dict]:
        """Fetch top stories from Hacker News"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Get top story IDs
                response = await client.get(f"{self.hn_base_url}/topstories.json")
                response.raise_for_status()
                story_ids = response.json()[:limit]
                
                # Fetch story details
                articles = []
                for story_id in story_ids:
                    story_response = await client.get(f"{self.hn_base_url}/item/{story_id}.json")
                    story_response.raise_for_status()
                    story = story_response.json()
                    
                    if story.get("type") == "story" and story.get("url"):
                        articles.append({
                            "title": story.get("title", ""),
                            "description": "",
                            "content": None,
                            "url": story.get("url", ""),
                            "source": "hackernews",
                            "source_id": str(story.get("id")),
                            "author": story.get("by", ""),
                            "published_at": datetime.fromtimestamp(story.get("time", 0)) if story.get("time") else None,
                            "upvotes": story.get("score", 0),
                            "comments": story.get("descendants", 0),
                            "tags": "news,tech",
                            "category": "general"
                        })
                
                return articles
        except httpx.HTTPError as e:
            logger.error(f"Hacker News API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching Hacker News: {e}")
            return []
    
    async def fetch_all_sources(self, limit: int = 30) -> List[dict]:
        """Fetch articles from all sources concurrently"""
        # Use asyncio.gather for concurrent requests
        import asyncio
        
        devto_articles = await self.fetch_devto_articles(limit)
        hn_articles = await self.fetch_hackernews_articles(limit)
        
        # Combine and deduplicate by URL
        all_articles = devto_articles + hn_articles
        
        # Remove duplicates (same URL from different sources)
        unique_articles = {}
        for article in all_articles:
            if article["url"] not in unique_articles:
                unique_articles[article["url"]] = article
        
        return list(unique_articles.values())