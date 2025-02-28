from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from app.services.video_service import create_templated_video
import os

router = APIRouter()

@router.post("/generate_video/")
async def generate_video(video_file: UploadFile = File(...), text_string: str = ""):
    try:
        # Save uploaded video temporarily (relative to project root)
        input_video_path = "temp_input_video.mp4"
        with open(input_video_path, "wb") as f:
            f.write(await video_file.read())

        # Define paths (relative paths will be converted to absolute in video_service)
        template_path = "static/template.png"
        output_path = "static/generated_videos/generated_output_video.mp4"

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Process the video
        create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(85, 250))

        # Return the generated video with the proper media type
        return FileResponse(output_path, media_type="video/mp4")

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
