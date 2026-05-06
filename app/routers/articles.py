from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article
from app.schemas import ArticleResponse, ArticleDetailResponse, PaginatedArticleResponse
from app.utils.errors import ArticleNotFound, InvalidPagination
from datetime import datetime

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/", response_model=PaginatedArticleResponse)
def list_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    source: str = Query(None),
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    List articles with pagination and filtering
    
    - **skip**: Number of articles to skip (default: 0)
    - **limit**: Number of articles to return (max: 100)
    - **source**: Filter by source (hackernews, devto, producthunt)
    - **category**: Filter by category (ai, web, devops, etc.)
    """
    query = db.query(Article).order_by(Article.published_at.desc())
    
    # Apply filters
    if source:
        query = query.filter(Article.source == source.lower())
    if category:
        query = query.filter(Article.category == category.lower())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    articles = query.offset(skip).limit(limit).all()
    
    total_pages = (total + limit - 1) // limit
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": total_pages,
        "items": articles
    }

@router.get("/{article_id}", response_model=ArticleDetailResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get article details by ID"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFound()
    
    # Increment view count
    article.view_count += 1
    db.commit()
    
    return article

@router.get("/search/", response_model=PaginatedArticleResponse)
def search_articles(
    q: str = Query(..., min_length=2, max_length=200),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search articles by title or description
    
    - **q**: Search query (minimum 2 characters)
    """
    query = db.query(Article).filter(
        (Article.title.ilike(f"%{q}%")) | 
        (Article.description.ilike(f"%{q}%"))
    ).order_by(Article.published_at.desc())
    
    total = query.count()
    articles = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": total_pages,
        "items": articles
    }
# Add to app/routers/articles.py

@router.get("/trending/", response_model=PaginatedArticleResponse)
def get_trending(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get trending articles (most upvotes + views in last 7 days)
    
    Trending score = upvotes * 2 + view_count
    """
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    last_7_days = datetime.utcnow() - timedelta(days=7)
    
    query = db.query(Article).filter(
        Article.published_at >= last_7_days
    ).order_by(
        (Article.upvotes * 2 + Article.view_count).desc()
    )
    
    total = query.count()
    articles = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": total_pages,
        "items": articles
    }

@router.get("/by-source/{source}", response_model=PaginatedArticleResponse)
def get_articles_by_source(
    source: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get articles filtered by source (hackernews, devto, producthunt)"""
    valid_sources = ["hackernews", "devto", "producthunt"]
    
    if source.lower() not in valid_sources:
        raise ValueError(f"Invalid source. Must be one of: {', '.join(valid_sources)}")
    
    query = db.query(Article).filter(
        Article.source == source.lower()
    ).order_by(Article.published_at.desc())
    
    total = query.count()
    articles = query.offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": total_pages,
        "items": articles
    }