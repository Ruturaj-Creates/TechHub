import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """Test user creation"""
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_user_duplicate_username():
    """Test duplicate username validation"""
    # Create first user
    client.post(
        "/users/",
        json={"username": "testuser", "email": "test1@example.com"}
    )
    
    # Try to create with same username
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test2@example.com"}
    )
    assert response.status_code == 400

def test_get_user(db):
    """Test getting user"""
    from app.models import User
    
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_get_user_not_found():
    """Test getting non-existent user"""
    response = client.get("/users/99999")
    assert response.status_code == 404

def test_update_user(db):
    """Test updating user"""
    from app.models import User
    
    user = User(username="oldname", email="old@example.com")
    db.add(user)
    db.commit()
    
    response = client.put(
        f"/users/{user.id}",
        json={"username": "newname"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newname"

def test_delete_user(db):
    """Test deleting user"""
    from app.models import User
    
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 404