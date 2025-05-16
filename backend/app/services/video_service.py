import cv2
import os
import time
import subprocess
import uuid
import openai
from openai import OpenAI
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import unicodedata

# Determine the project root directory.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def generate_caption(user_prompt):
    prompt = (
        "Write a short, professional Instagram caption (1-2 sentences and under 200 words) for a D1 college soccer highlight clip from UC Davis. "
        "The tone should match high-level football accounts like the Premier League or Champions League. "
        "Make it VERY energetic, confident, and focused on the moment — no emojis, no hashtags. "
        "Highlight the action (goal, assist, tackle, save, etc.) and its impact on the game. "
        "Insert a line break (\\n) every 7-8 words or 50 characters max (new line after word is complete only) (max 4 lines only!!!!) in the caption to improve visual structure. "
        "Make 100% sure it has no emojis or hashtags. No characters other than text!!!!very important."
        + user_prompt
    )
    Api_Key = ["insert your api key here"]  # Replace with your actual API key
    client = OpenAI(api_key=Api_Key)
    print("Generating caption...")
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a sports caption writer for Instagram."},
            {"role": "user", "content": prompt}
        ]
    )
    caption = response.choices[0].message.content
    print(f"Generated string: {caption}")
    return caption

def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(100, 1150)):
    try:
        input_video_path = os.path.join(BASE_DIR, input_video_path)
        template_path = os.path.join(BASE_DIR, template_path)
        output_dir = os.path.dirname(os.path.join(BASE_DIR, output_path))
        os.makedirs(output_dir, exist_ok=True)
        final_output = os.path.join(output_dir, f"generated_output_video_{uuid.uuid4().hex}.mp4")

        target_width, target_height = 1080, 1350

        # Load template
        if not os.path.exists(template_path):
            raise Exception(f"Template image not found at: {template_path}")
        template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template_img is None:
            raise Exception("Failed to load template image")
        template_img = cv2.resize(template_img, (target_width, target_height))
        if template_img.shape[2] == 4:
            template_img = cv2.cvtColor(template_img, cv2.COLOR_BGRA2BGR)

        # Open video
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise Exception("Failed to open input video")
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = input_width / input_height

        overlay_width = 920
        overlay_height = int(overlay_width / aspect_ratio)
        overlay_width = min(overlay_width, target_width)
        overlay_height = min(overlay_height, target_height)

        temp_output = os.path.join(output_dir, "temp_generated_video.mp4")
        out = cv2.VideoWriter(temp_output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (target_width, target_height))
        print(f"Saving video to: {temp_output}")

        text_string = generate_caption(text_string)
        text_string = text_string.replace('\\n', '\n')
        text_string = unicodedata.normalize("NFKD", text_string)
        lines = text_string.split('\n')

        font_path = os.path.join(BASE_DIR, "static/fonts/Roboto_Condensed-Bold.ttf")
        if not os.path.exists(font_path):
            raise Exception(f"Font file not found at: {font_path}")
        font = ImageFont.truetype(font_path, size=45)

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
            result = template_img.copy()
            y1, y2 = video_pos[1], video_pos[1] + overlay_video.shape[0]
            x1, x2 = video_pos[0], video_pos[0] + overlay_video.shape[1]
            result[y1:y2, x1:x2] = overlay_video

            # Convert frame to PIL
            result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(result_pil)

            # Draw each line
            y_offset = 820
            for line in lines:
                if line.strip():
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_x = (target_width - text_width) // 2
                    draw.text((text_x, y_offset), line, font=font, fill=(255, 255, 255))
                    y_offset += 70

            result = cv2.cvtColor(np.array(result_pil), cv2.COLOR_RGB2BGR)
            out.write(result)

            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")

        out.release()
        cap.release()
        cv2.destroyAllWindows()

        # Ensure file is flushed
        prev_size, stable = -1, False
        while not stable:
            time.sleep(0.1)
            current_size = os.path.getsize(temp_output)
            stable = current_size == prev_size
            prev_size = current_size

        # Re-encode with ffmpeg
        final_ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", temp_output,
            "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.0",
            "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "22",
            "-movflags", "+faststart", final_output
        ]
        print("Running ffmpeg re-encoding...")
        subprocess.run(final_ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(temp_output)

        print(f"Final video created: {final_output}")
        return final_output

    except Exception as e:
        print(f"An error occurred in create_templated_video: {str(e)}")
        if 'cap' in locals(): cap.release()
        if 'out' in locals(): out.release()
        cv2.destroyAllWindows()
        raise e
