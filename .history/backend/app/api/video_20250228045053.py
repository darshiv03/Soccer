import json
import os
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from app.services.video_service import create_templated_video

router = APIRouter()

# Path to store history
HISTORY_FILE = "history.json"

def save_to_history(query, video_filename, num_clips=1):
    """ Saves query, result, and video link to history.json """
    history_entry = {
        "query": query,
        "video_url": f"/static/generated_videos/{video_filename}",
        "num_clips": num_clips
    }

    # Load existing history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)
    else:
        history = []

    # Append new entry & save
    history.append(history_entry)
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

@router.post("/generate_video/")
async def generate_video(video_file: UploadFile = File(...), text_string: str = ""):
    try:
        # Save uploaded video temporarily
        input_video_path = "temp_input_video.mp4"
        with open(input_video_path, "wb") as f:
            f.write(await video_file.read())

        template_path = "static/template.png"
        output_path = "static/generated_videos/generated_output_video.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Generate video
        final_video_path = create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(85, 250))

        # Extract filename for history tracking
        video_filename = os.path.basename(final_video_path)
        save_to_history(text_string, video_filename, num_clips=1)

        return FileResponse(final_video_path, media_type="video/mp4", headers={"Cache-Control": "no-store"})

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@router.get("/history/")
async def get_history():
    """ Fetches the stored video generation history """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)
        return history
    return []
