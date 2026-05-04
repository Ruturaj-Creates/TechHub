from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """application configuration"""
    database_url: str = "sqlite:///./test.db"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # API Keys
    dev_to_api_key: str = ""
    news_api_key: str = ""
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Get settings (cached for performance)"""
    return Settings()
