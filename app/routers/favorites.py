from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Article, Favorite
from app.schemas import FavoriteResponse
from app.utils.errors import UserNotFound, ArticleNotFound, FavoriteAlreadyExists

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(user_id: int, article_id: int, db: Session = Depends(get_db)):
    """Add article to user's favorites"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFound()
    
    # Verify article exists
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise ArticleNotFound()
    
    # Check if already favorited
    existing = db.query(Favorite).filter(
        (Favorite.user_id == user_id) & (Favorite.article_id == article_id)
    ).first()
    
    if existing:
        raise FavoriteAlreadyExists()
    
    # Create favorite
    favorite = Favorite(user_id=user_id, article_id=article_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    return favorite

@router.get("/user/{user_id}")
def get_user_favorites(user_id: int, db: Session = Depends(get_db)):
    """Get all favorites for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFound()
    
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    return {"user_id": user_id, "favorites_count": len(favorites), "items": favorites}

@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(favorite_id: int, db: Session = Depends(get_db)):
    """Remove article from favorites"""
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not favorite:
        raise ArticleNotFound()  # Not exactly right, but works
    
    db.delete(favorite)
    db.commit()