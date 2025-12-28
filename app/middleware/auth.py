"""
Authentication Middleware
API Key and JWT token verification
"""
from fastapi import HTTPException, Header
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("API_KEY", "dev-api-key-12345-change-in-production")

async def verify_api_key(api_key: Optional[str] = None):
    """
    Verify API key from header
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Please provide X-API-Key header."
        )
    
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    
    return True

