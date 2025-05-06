from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import verify_google_token

router = APIRouter()

class TokenRequest(BaseModel):
    token: str

@router.post("/google")
async def google_auth(request: TokenRequest):
    try:
        result = await verify_google_token(request.token)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) 