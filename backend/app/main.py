from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.video import router as video_router
from app.api.auth import router as auth_router
from app.config import CORS_ORIGINS, API_V1_PREFIX

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(video_router, prefix=API_V1_PREFIX, tags=["Video"])
app.include_router(auth_router, prefix=f"{API_V1_PREFIX}/auth", tags=["Auth"])
