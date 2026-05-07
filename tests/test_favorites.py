import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Article
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def sample_data(db):
    """Create sample user and article"""
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.flush()
    
    article = Article(
        title="Test Article",
        url="https://example.com/test",
        source="devto",
        source_id="1",
        published_at=datetime.utcnow()
    )
    db.add(article)
    db.commit()
    
    return {"user": user, "article": article}

def test_add_favorite(sample_data):
    """Test adding to favorites"""
    user_id = sample_data["user"].id
    article_id = sample_data["article"].id
    
    response = client.post(
        f"/favorites/?user_id={user_id}&article_id={article_id}"
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["article_id"] == article_id

def test_add_favorite_duplicate(sample_data):
    """Test adding duplicate favorite"""
    user_id = sample_data["user"].id
    article_id = sample_data["article"].id
    
    # Add first favorite
    client.post(f"/favorites/?user_id={user_id}&article_id={article_id}")
    
    # Try to add again
    response = client.post(
        f"/favorites/?user_id={user_id}&article_id={article_id}"
    )
    assert response.status_code == 400

def test_get_user_favorites(sample_data):
    """Test getting user favorites"""
    user_id = sample_data["user"].id
    article_id = sample_data["article"].id
    
    # Add favorite
    client.post(f"/favorites/?user_id={user_id}&article_id={article_id}")
    
    # Get favorites
    response = client.get(f"/favorites/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["favorites_count"] >= 1

def test_remove_favorite(sample_data, db):
    """Test removing favorite"""
    from app.models import Favorite
    
    user_id = sample_data["user"].id
    article_id = sample_data["article"].id
    
    # Add favorite
    favorite = Favorite(user_id=user_id, article_id=article_id)
    db.add(favorite)
    db.commit()
    
    # Remove favorite
    response = client.delete(f"/favorites/{favorite.id}")
    assert response.status_code == 204