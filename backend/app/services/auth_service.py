from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
import os
from datetime import datetime, timedelta
from jose import jwt

# These should be in your environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")  # Change this in production
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def verify_google_token(token: str):
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        # Get user info
        user_info = {
            "email": idinfo["email"],
            "name": idinfo.get("name", ""),
            "picture": idinfo.get("picture", ""),
            "sub": idinfo["sub"]  # Google's unique user ID
        }
        
        # Create access token
        access_token = create_access_token(user_info)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": user_info
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_access_token(user_info: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user_info["sub"],
        "email": user_info["email"],
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt 