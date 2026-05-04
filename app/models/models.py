from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    """User model for storing user accounts"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    read_history = relationship("ReadHistory", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Article(Base):
    """Article model for storing aggregated tech news"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    
    # Article metadata
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String(500), unique=True, nullable=False)
    
    # Source information
    source = Column(String(50), nullable=False, index=True)  # "hackernews", "devto", "producthunt"
    source_id = Column(String(100), nullable=False, index=True)  # External source ID
    
    # Author & timestamps
    author = Column(String(100), nullable=True)
    published_at = Column(DateTime, nullable=True, index=True)
    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Engagement metrics
    upvotes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    # Category/Tags
    tags = Column(String(200), nullable=True)  # Comma-separated
    category = Column(String(50), nullable=True, index=True)  # "ai", "web", "devops", etc.
    
    # Relationships
    favorites = relationship("Favorite", back_populates="article", cascade="all, delete-orphan")
    read_history = relationship("ReadHistory", back_populates="article", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Article(id={self.id}, title={self.title[:50]}..., source={self.source})>"


class Favorite(Base):
    """User's favorite articles"""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="favorites")
    article = relationship("Article", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, article_id={self.article_id})>"


class ReadHistory(Base):
    """Track articles user has read"""
    __tablename__ = "read_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    read_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="read_history")
    article = relationship("Article", back_populates="read_history")

    def __repr__(self):
        return f"<ReadHistory(user_id={self.user_id}, article_id={self.article_id})>"