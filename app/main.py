from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import users, articles, favorites

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="TechHub - Tech News Aggregator",
    description="Aggregate and discover tech news from Hacker News, Dev.to, and Product Hunt",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(favorites.router)

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "TechHub API is running"}

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to TechHub - Tech News Aggregator",
        "docs": "/docs",
        "docs_redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)