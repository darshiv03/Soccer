from pydantic import BaseModel
from typing import Tuple

class VideoRequest(BaseModel):
    text_string: str
    video_pos: Tuple[int, int] = (100, 1150)
    template_path: str = "template.png"  # Default path or could be dynamic
    output_filename: str = "output_video.mp4"
