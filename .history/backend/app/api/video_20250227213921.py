from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.video_service import create_templated_video
from backend.app.models.models import VideoRequest  # Optional: Pydantic model for request validation
import shutil
import os

router = APIRouter()

@router.post("/generate_video/")
async def generate_video(request: VideoRequest, video_file: UploadFile = File(...), template_file: UploadFile = File(...)):
    try:
        # Create temporary files for the uploaded video and template image
        temp_video_path = f"temp_{video_file.filename}"
        temp_template_path = f"temp_{template_file.filename}"

        # Save the uploaded files
        with open(temp_video_path, "wb") as video_buffer:
            shutil.copyfileobj(video_file.file, video_buffer)
        
        with open(temp_template_path, "wb") as template_buffer:
            shutil.copyfileobj(template_file.file, template_buffer)

        # Define the output path for the generated video
        output_path = os.path.join("output", request.output_filename)

        # Call the function to create the templated video
        create_templated_video(temp_video_path, request.text_string, output_path, temp_template_path, video_pos=request.video_pos)

        # Return the generated video
        return FileResponse(output_path, media_type="video/mp4", filename=request.output_filename)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    finally:
        # Clean up temporary files
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if os.path.exists(temp_template_path):
            os.remove(temp_template_path)
