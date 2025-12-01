"""
Configuration for standalone MCP client
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Class for managing MCP client configuration"""
    
    def __init__(self, api_key: str, api_url: str):
        """
        Initialize configuration
        
        Args:
            api_key: API key for authentication
            api_url: API server URL
        """
        self.api_key = api_key
        self.api_url = api_url
    
    @classmethod
    def load(cls) -> 'Config':
        """
        Load configuration from environment variables
        
        Loading order:
        1. Environment variables
        2. .env file in current directory
        
        Returns:
            Config: Configuration object
        
        Raises:
            ValueError: If required parameters are not set
        """
        # Load .env file from current directory
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        
        # Get parameters from environment variables
        api_key = os.getenv("MCP_API_KEY") or os.getenv("API_KEY")
        api_url = os.getenv("MCP_API_URL") or os.getenv("API_URL")
        
        # Validation
        if not api_key:
            raise ValueError(
                "API_KEY is not set. Please set MCP_API_KEY or API_KEY environment variable "
                "or create a .env file with API_KEY=your_key"
            )
        
        if not api_url:
            raise ValueError(
                "API_URL is not set. Please set MCP_API_URL or API_URL environment variable "
                "or create a .env file with API_URL=https://your-server.com"
            )
        
        # Check API key format
        if not api_key.startswith("sk_"):
            raise ValueError(
                f"Invalid API key format. API key should start with 'sk_', got: {api_key[:10]}..."
            )
        
        # Check URL format
        if not api_url.startswith(("http://", "https://")):
            raise ValueError(
                f"Invalid API URL format. URL should start with 'http://' or 'https://', got: {api_url}"
            )
        
        return cls(api_key=api_key, api_url=api_url)
    
    def __repr__(self) -> str:
        return f"Config(api_key={self.api_key[:10]}..., api_url={self.api_url})"

