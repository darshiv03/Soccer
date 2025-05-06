from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.video import router as video_router
from app.api.auth import router as auth_router

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(video_router, prefix="/api", tags=["Video"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
