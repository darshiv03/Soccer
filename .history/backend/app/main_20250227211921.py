from fastapi import FastAPI
from app.api.video import router as video_router

app = FastAPI()

# Include the video processing route
app.include_router(video_router, prefix="/api", tags=["Video"])
