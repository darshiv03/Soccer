from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
from fastapi.security import HTTPAuthorizationCredentials
from app.services.video_service import create_templated_video
from app.services.history_service import save_to_history, get_history
from app.middleware.auth import JWTAuthMiddleware
import os
from typing import Optional

router = APIRouter()
auth_middleware = JWTAuthMiddleware()

def get_template_path(template_id: str) -> str:
    template_map = {
        "template1": "static/template1.png",
        "template2": "static/template2.png",
        "template3": "static/template3.png",
        "template4": "static/template4.png",
        "template5": "static/template5.png",
    }
    return template_map.get(template_id, "static/templates/template1.png")

@router.post("/video/generate")
async def generate_video(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    template: str = Form("template1"),
    negative_prompt: str = Form(""),
    num_inference_steps: int = Form(20),
    guidance_scale: float = Form(7.5),
    num_frames: int = Form(24),
    fps: int = Form(24),
    seed: Optional[int] = Form(None),
    credentials: HTTPAuthorizationCredentials = Depends(auth_middleware)
):
    try:
        # Save uploaded video
        input_video_path = "temp_input_video.mp4"
        with open(input_video_path, "wb") as f:
            f.write(await file.read())

        template_path = get_template_path(template)
        output_path = "static/generated_videos/generated_output_video.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        final_video_path = create_templated_video(
            input_video_path=input_video_path,
            text_string=prompt,
            output_path=output_path,
            template_path=template_path,
            video_pos=(85, 250)
        )

        video_filename = os.path.basename(final_video_path)
        video_url = f"http://127.0.0.1:8000/static/generated_videos/{video_filename}"

        save_to_history(prompt, video_filename, num_clips=1)

        return {"video_url": video_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

@router.get("/history")
async def fetch_history(credentials: HTTPAuthorizationCredentials = Depends(auth_middleware)):
    try:
        return get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History error: {str(e)}")
