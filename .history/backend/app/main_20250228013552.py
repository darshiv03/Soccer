import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.video import router as video_router

# Set up logging to display print/logging messages
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI()

# Serve static files (like images, videos, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, change this in production!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include video processing routes
app.include_router(video_router, prefix="/api", tags=["Video"])

@app.get("/")
async def root():
    # Example of logging
    logger.info("This is an info message")
    
    # Example of print statement
    print("This is a print statement")

    return {"message": "Hello World"}
