# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.video import router as video_router

# app = FastAPI()

# # CORS setup: allow requests from any origin (for local development)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # This allows all origins, change this in production!
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# # Include the video processing route
# app.include_router(video_router, prefix="/api", tags=["Video"])

# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.video import router as video_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, change this in production!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include video processing routes
app.include_router(video_router, prefix="/api", tags=["Video"])
