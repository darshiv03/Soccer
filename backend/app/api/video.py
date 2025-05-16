from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.services.video_service import create_templated_video
from app.services.history_service import save_to_history, get_history
from app.middleware.auth import JWTAuthMiddleware
from fastapi.security import HTTPAuthorizationCredentials
import os
from typing import Optional

router = APIRouter()
auth_middleware = JWTAuthMiddleware()

@router.post("/video/generate")
async def generate_video(
    file: UploadFile = File(...),
    prompt: str = "",
    negative_prompt: str = "",
    num_inference_steps: int = 20,
    guidance_scale: float = 7.5,
    num_frames: int = 24,
    fps: int = 24,
    seed: Optional[int] = None,
    credentials: HTTPAuthorizationCredentials = Depends(auth_middleware)
):
    try:
        # Save uploaded video temporarily (relative to project root)
        input_video_path = "temp_input_video.mp4"
        with open(input_video_path, "wb") as f:
            f.write(await file.read())

        template_path = "static/template.png"
        output_path = "static/generated_videos/generated_output_video.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        final_video_path = create_templated_video(
            input_video_path, 
            prompt, 
            output_path, 
            template_path, 
            video_pos=(85, 250)
        )
        
        video_filename = final_video_path.split(os.path.sep)[-1]  # Extract filename
        video_url = f"http://127.0.0.1:8000/static/generated_videos/{video_filename}"

        # Save query to history
        save_to_history(prompt, video_filename, num_clips=1)

        return {"video_url": video_url}

    except Exception as e:
        error_msg = f"An error occurred in generate_video: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/history")
async def fetch_history(credentials: HTTPAuthorizationCredentials = Depends(auth_middleware)):
    """ Fetches the stored video generation history """
    try:
        return get_history()
    except Exception as e:
        error_msg = f"An error occurred while fetching history: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
