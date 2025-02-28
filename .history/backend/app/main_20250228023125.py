from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.video import router as video_router

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, change this in production!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include video processing routes
app.include_router(video_router, prefix="/api", tags=["Video"])
