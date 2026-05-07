import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def sample_articles(db):
    """Create sample articles for testing"""
    from app.models import Article
    
    articles = [
        Article(
            title="FastAPI Tutorial",
            url="https://example.com/fastapi",
            source="devto",
            source_id="1",
            published_at=datetime.utcnow(),
            category="web"
        ),
        Article(
            title="Python Tips",
            url="https://example.com/python",
            source="hackernews",
            source_id="2",
            published_at=datetime.utcnow(),
            category="python"
        )
    ]
    
    for article in articles:
        db.add(article)
    db.commit()
    
    return articles

def test_list_articles(sample_articles):
    """Test listing articles"""
    response = client.get("/articles/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2

def test_list_articles_with_pagination():
    """Test pagination"""
    response = client.get("/articles/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data

def test_get_article(sample_articles):
    """Test getting single article"""
    article = sample_articles[0]
    response = client.get(f"/articles/{article.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "FastAPI Tutorial"

def test_get_article_not_found():
    """Test getting non-existent article"""
    response = client.get("/articles/99999")
    assert response.status_code == 404

def test_search_articles(sample_articles):
    """Test article search"""
    response = client.get("/articles/search/?q=fastapi")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1

def test_search_no_results():
    """Test search with no results"""
    response = client.get("/articles/search/?q=nonexistent123456")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0

def test_trending_articles(sample_articles):
    """Test getting trending articles"""
    response = client.get("/articles/trending/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data

def test_articles_by_source(sample_articles):
    """Test filtering by source"""
    response = client.get("/articles/by-source/devto")
    assert response.status_code == 200
    data = response.json()
    # Check all returned articles are from devto
    for article in data["items"]:
        assert article["source"] == "devto"