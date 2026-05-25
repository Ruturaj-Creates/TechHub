# TechHub - Tech News Aggregator

A FastAPI backend for aggregating tech news from Hacker News, Dev.to, and Product Hunt.

## Features
- ✅ Aggregate news from multiple sources
- ✅ User accounts and favorites
- ✅ Search and filter articles
- ✅ Personalized recommendations (Day 2)
- ✅ Read history tracking

## Tech Stack
- FastAPI
- PostgreSQL (Day 2)
- SQLAlchemy ORM
- Pydantic validation

## Setup (Development)

### Prerequisites
- Python 3.9+
- PostgreSQL (for production; SQLite for dev)

### Installation

1. Clone and setup:
```bash
git clone <repo>
cd TechHub
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create `.env`:
```env
DATABASE_URL=sqlite:///./test.db
ENVIRONMENT=development
DEBUG=True
```

3. Run migrations and start server:
```bash
python -m uvicorn app.main:app --reload
```

4. Visit http://localhost:8000/docs for interactive API docs

## API Endpoints

### Users
- `POST /users/` - Create user
- `GET /users/{user_id}` - Get user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Articles
- `GET /articles/` - List articles (with pagination)
- `GET /articles/{article_id}` - Get article details
- `GET /articles/search/?q=query` - Search articles

### Favorites
- `POST /favorites/?user_id=1&article_id=5` - Add favorite
- `GET /favorites/user/{user_id}` - Get user favorites
- `DELETE /favorites/{favorite_id}` - Remove favorite

## Next Steps 
- Integrate external APIs (NewsAPI, Dev.to, Hacker News)
- Add async background tasks
- Implement caching
- Add more advanced filtering

## Learning Goals
- ✅ FastAPI project structure
- ✅ SQLAlchemy ORM
- ✅ Pydantic validation
- ✅ Proper HTTP status codes
- ✅ Git workflow (branching, committing)
- ✅ External API integration 
- ✅ Async/await patterns
- ✅ Testing 

## Future Improvements

- JWT Authentication
- Docker support
- Redis caching
- AI-based recommendations
- Rate limiting
- CI/CD pipeline