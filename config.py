"""
Configuration settings for the Market Research Agent system.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for API keys and settings."""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY") 
    EXA_API_KEY: Optional[str] = os.getenv("EXA_API_KEY")
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    
    # Optional API Keys
    KAGGLE_USERNAME: Optional[str] = os.getenv("KAGGLE_USERNAME")
    KAGGLE_KEY: Optional[str] = os.getenv("KAGGLE_KEY")
    
    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    
    # Debug Settings
    ENABLE_DEBUG: bool = os.getenv("ENABLE_DEBUG", "false").lower() == "true"
    
    @classmethod
    def validate_required_keys(cls) -> list[str]:
        """Validate that required API keys are present."""
        missing_keys = []
        
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not cls.TAVILY_API_KEY:
            missing_keys.append("TAVILY_API_KEY")
            
        return missing_keys
    
    @classmethod
    def is_configured(cls) -> bool:
        """Check if minimum required configuration is present."""
        return len(cls.validate_required_keys()) == 0

# Create global config instance
config = Config()
