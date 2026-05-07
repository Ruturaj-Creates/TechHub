# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-05-05

### Added
- User management endpoints (create, read, update, delete)
- Article aggregation from multiple sources (Dev.to, Hacker News)
- Article search and filtering
- Trending articles endpoint
- User favorites management
- Read history tracking
- Automatic background task scheduling
- Comprehensive test suite
- Docker and Docker Compose setup
- API documentation with Swagger UI
- PostgreSQL support for production

### Infrastructure
- FastAPI web framework
- SQLAlchemy ORM with PostgreSQL
- APScheduler for background tasks
- pytest for testing
- Docker containerization

## [0.1.0] - 2024-05-06

### Added
- Initial project setup
- Database models (User, Article, Favorite, ReadHistory)
- Basic CRUD endpoints
- Pydantic validation schemas