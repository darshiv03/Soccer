from fastapi import APIRouter, File, UploadFile
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
        # The output_path here is a placeholder; create_templated_video generates a unique filename.
        output_path = "static/generated_videos/generated_output_video.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        final_video_path = create_templated_video(
            input_video_path,
            text_string,
            output_path,
            template_path,
            video_pos=(85, 250)
        )
        # Convert the absolute path to a URL that your static mount serves.
        video_url = f"http://127.0.0.1:8000/static/generated_videos/{final_video_path.split(os.path.sep)[-1]}"
        print("Returning video URL:", video_url)
        return {"video_url": video_url}

    except Exception as e:
        error_msg = f"An error occurred in generate_video: {str(e)}"
        print(error_msg)
        return {"error": error_msg}
