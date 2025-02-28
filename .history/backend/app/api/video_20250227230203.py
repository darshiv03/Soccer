# app/api/video.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from app.services.video_service import create_templated_video

router = APIRouter()

@router.post("/generate_video/")
async def generate_video(video_file: UploadFile = File(...), text_string: str = ""):
    try:
        # Save the uploaded video to a temporary location
        temp_video_path = f"temp_{video_file.filename}"
        with open(temp_video_path, "wb") as video_buffer:
            shutil.copyfileobj(video_file.file, video_buffer)

        # Define the output path for the generated video
        output_path = "generated_videos/generated_output_video.mp4"  # Ensure this directory exists

        # Call the video processing service
        create_templated_video(temp_video_path, text_string, output_path, "template.png", video_pos=(85, 250))

        # Return the generated video as a response
        return FileResponse(output_path, media_type="video/mp4", filename="generated_output_video.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Clean up temporary files
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
