from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from app.services.video_service import create_templated_video
import os

router = APIRouter()

@router.post("/generate_video/")
async def generate_video(video_file: UploadFile = File(...), text_string: str = ""):
    try:
        # Save uploaded video temporarily
        input_video_path = "temp_input_video.mp4"
        with open(input_video_path, "wb") as f:
            f.write(await video_file.read())

        # Define paths
        template_path = "static/template.png"  # Path to the template image
        output_path = "static/generated_videos/generated_output_video.mp4"  # Path to save the generated video

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Call the video processing function
        create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(85, 250))

        # Return the generated video as a response
        return FileResponse(output_path)

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
