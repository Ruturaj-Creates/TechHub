from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db,get_db
from app.routers import users, articles, favorites
from app.services.scheduler import scheduler

# Startup/Shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting TechHub API...")
    scheduler.start()
    yield
    # Shutdown
    print("Shutting down TechHub API...")
    scheduler.stop()

# Create FastAPI app with lifespan
app = FastAPI(
    title="TechHub - Tech News Aggregator",
    description="Aggregate and discover tech news from Hacker News, Dev.to, and Product Hunt",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize database
init_db()

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

# New endpoint to manually trigger article fetch
@app.post("/admin/refresh-articles")
async def refresh_articles(db = Depends(get_db)):
    """Manually trigger article refresh"""
    from app.services.ingest_service import IngestionService
    result = await IngestionService.ingest_articles(db, limit=50)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)