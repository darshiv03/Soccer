from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt
from app.config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    GOOGLE_CLIENT_ID
)

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
        "name": user_info.get("name", ""),
        "picture": user_info.get("picture", ""),
        "exp": int(expire.timestamp())  # Convert to Unix timestamp
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_user_from_token(token: str) -> dict:
    """Extract user information from a JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {
            "email": payload["email"],
            "name": payload.get("name", ""),
            "picture": payload.get("picture", ""),
            "sub": payload["sub"]
        }
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token") 