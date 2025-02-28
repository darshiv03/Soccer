from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from app.services.video_service import create_templated_video
import os

router = APIRouter()

@router.post("/generate_video/")
async def generate_video(video_file: UploadFile = File(...), text_string: str = ""):
    try:
        # Save the uploaded video temporarily (relative to project root)
        input_video_path = "temp_input_video.mp4"
        with open(input_video_path, "wb") as f:
            f.write(await video_file.read())

        template_path = "static/template.png"
        # The output_path is a placeholder; the service will generate a unique filename.
        output_path = "static/generated_videos/generated_output_video.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        final_video_path = create_templated_video(
            input_video_path,
            text_string,
            output_path,
            template_path,
            video_pos=(85, 250)
        )
        # Return the generated video with proper media type and no caching.
        return FileResponse(final_video_path, media_type="video/mp4", headers={"Cache-Control": "no-store"})

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
