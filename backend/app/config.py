from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    # Required API keys
    openai_api_key: str
    hardcover_api_key: str = ""  # Optional, can be empty
    
    # OpenAI-compatible API configuration (for Groq support)
    openai_base_url: str = "https://api.openai.com/v1"  # Default to OpenAI, can override for Groq
    
    # Cache settings
    cache_dir: str = "cache"
    cache_expire_seconds: int = 3600  # 1 hour
    book_cache_expire_seconds: int = 86400  # 24 hours (books don't change often)
    taste_profile_cache_expire_seconds: int = 7200  # 2 hours (taste profiles are more dynamic)
    
    # API rate limiting
    max_movies_per_request: int = 5
    gpt_max_tokens: int = 1200  # Increased for more detailed responses
    gpt_temperature: float = 0.7
    gpt_model: str = "gpt-4o-mini"  # Can be overridden for other providers like Groq
    
    # Recommendation settings
    books_per_recommendation: int = 5  # Number of books to recommend
    default_recommendation_type: str = "unified"  # "unified" or "individual"
    enable_taste_profile_analysis: bool = True
    enable_recommendation_insights: bool = True
    
    # Book metadata enhancement
    enable_hardcover_integration: bool = True  # Enable Hardcover integration for book metadata
    hardcover_timeout_seconds: int = 10
    hardcover_retry_attempts: int = 3
    
    # Performance settings
    enable_concurrent_processing: bool = True
    max_concurrent_book_requests: int = 10
    request_timeout_seconds: int = 30
    
    # Development settings
    debug: bool = False
    log_level: str = "INFO"
    enable_metrics: bool = True
    
    # Feature flags
    enable_alternative_suggestions: bool = True
    enable_genre_analysis: bool = True
    enable_complexity_scoring: bool = True
    enable_taste_matching: bool = True

settings = Settings()