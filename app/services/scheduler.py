import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.ingest_service import IngestionService

logger = logging.getLogger(__name__)

class NewsScheduler:
    """Background scheduler for periodic news fetching"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
    
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            # Schedule article fetching every hour
            self.scheduler.add_job(
                self._fetch_articles,
                IntervalTrigger(hours=1),
                id="fetch_articles",
                name="Fetch articles from all sources",
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            logger.info("News scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("News scheduler stopped")
    
    def _fetch_articles(self):
        """Fetch articles (runs in background)"""
        db = SessionLocal()
        try:
            import asyncio
            asyncio.run(IngestionService.ingest_articles(db, limit=50))
        except Exception as e:
            logger.error(f"Scheduled fetch failed: {e}")
        finally:
            db.close()

# Global scheduler instance
scheduler = NewsScheduler()