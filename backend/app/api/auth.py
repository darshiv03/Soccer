from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import verify_google_token, get_user_from_token
from app.middleware.auth import JWTAuthMiddleware
from jose import JWTError

router = APIRouter()
auth_middleware = JWTAuthMiddleware()

class TokenRequest(BaseModel):
    token: str

@router.post("/google")
async def google_auth(request: TokenRequest):
    try:
        result = await verify_google_token(request.token)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/verify")
async def verify_token(request: TokenRequest):
    try:
        # First verify the token structure and expiration
        if not auth_middleware.verify(request.token):
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Then get the user info
        try:
            user_info = get_user_from_token(request.token)
            return {"valid": True, "user": user_info}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}") 