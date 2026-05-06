import logging
from sqlalchemy.orm import Session
from app.models import Article
from app.services.news_service import NewsService

logger = logging.getLogger(__name__)
news_service = NewsService()

class IngestionService:
    """Service for ingesting articles into database"""
    
    @staticmethod
    async def ingest_articles(db: Session, limit: int = 50):
        """Fetch articles from all sources and store in database"""
        try:
            # Fetch articles from all sources
            articles_data = await news_service.fetch_all_sources(limit)
            
            ingested = 0
            failed = 0
            
            for article_data in articles_data:
                try:
                    # Check if article already exists
                    existing = db.query(Article).filter(
                        Article.url == article_data["url"]
                    ).first()
                    
                    if not existing:
                        # Create new article
                        article = Article(**article_data)
                        db.add(article)
                        ingested += 1
                    else:
                        # Update existing article with new metrics
                        existing.upvotes = article_data.get("upvotes", existing.upvotes)
                        existing.comments = article_data.get("comments", existing.comments)
                        db.merge(existing)
                except Exception as e:
                    logger.error(f"Failed to ingest article: {e}")
                    failed += 1
                    continue
            
            # Commit all changes
            db.commit()
            logger.info(f"Ingestion complete: {ingested} new, {failed} failed")
            return {"ingested": ingested, "failed": failed}
        
        except Exception as e:
            logger.error(f"Ingestion service error: {e}")
            db.rollback()
            raise

# Usage in router:
# result = await IngestionService.ingest_articles(db)