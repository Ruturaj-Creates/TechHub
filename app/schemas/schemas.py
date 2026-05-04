from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# ============ User Schemas ============
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserUpdate(BaseModel):
    """Schema for updating user"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Article Schemas ============
class ArticleCreate(BaseModel):
    """Schema for creating article (internal use)"""
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    source: str
    source_id: str
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    upvotes: int = 0
    comments: int = 0
    tags: Optional[str] = None
    category: Optional[str] = None

class ArticleUpdate(BaseModel):
    """Schema for updating article metrics"""
    upvotes: Optional[int] = None
    comments: Optional[int] = None
    view_count: Optional[int] = None

class ArticleResponse(BaseModel):
    """Schema for article response"""
    id: int
    title: str
    description: Optional[str]
    url: str
    source: str
    author: Optional[str]
    published_at: Optional[datetime]
    upvotes: int
    comments: int
    view_count: int
    tags: Optional[str]
    category: Optional[str]
    fetched_at: datetime

    class Config:
        from_attributes = True

class ArticleDetailResponse(ArticleResponse):
    """Extended article response with content"""
    content: Optional[str]


# ============ Favorite Schemas ============
class FavoriteCreate(BaseModel):
    """Schema for creating favorite"""
    user_id: int
    article_id: int

class FavoriteResponse(BaseModel):
    """Schema for favorite response"""
    id: int
    user_id: int
    article_id: int
    created_at: datetime
    article: ArticleResponse  # Include article details

    class Config:
        from_attributes = True


# ============ Pagination Schemas ============
class PaginatedArticleResponse(BaseModel):
    """Schema for paginated article response"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[ArticleResponse]

    class Config:
        from_attributes = True