import cv2
import os
import time
import subprocess
import uuid
import openai  
from openai import OpenAI


# Determine the project root directory.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
def generate_caption(user_prompt):
    prompt = (
        "Write a short, professional Instagram caption (1-2 sentences) for a D1 college soccer highlight clip from UC Davis. The tone should match high-level football accounts like the Premier League or Champions League. Make it VERY energetic, confident, and focused on the moment — no emojis, no hashtags. Highlight the action (goal, assist, tackle, save, etc.) and its impact on the game. Insert a line break (\n) every 8-9 words in the caption to improve visual structure."
        + user_prompt
    )
    Api_Key = "[insert api key]"
    client = OpenAI(api_key= Api_Key)  # Replace with your actual API key
    print("Delete: Before response")
    response = client.chat.completions.create(
        model="gpt-4.1",  
        messages=[
            {"role": "system", "content": "You are a sports caption writer for Instagram."},
            {"role": "user", "content": prompt}
        ]
    )
    print(f"Generated string {response.choices[0].message.content}")
    return response.choices[0].message.content

def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(100, 1150)):
    try:
        # Debug logging for text_string
        print(f"Received text_string: '{text_string}'")
        print(f"Text string type: {type(text_string)}")
        print(f"Text string length: {len(text_string) if text_string else 0}")
        
        # Convert provided paths (relative to project root) to absolute paths
        input_video_path = os.path.join(BASE_DIR, input_video_path)
        template_path = os.path.join(BASE_DIR, template_path)
        
        # Prepare the output directory and generate a unique final filename.
        output_dir = os.path.dirname(os.path.join(BASE_DIR, output_path))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        unique_id = uuid.uuid4().hex
        final_output = os.path.join(output_dir, f"generated_output_video_{unique_id}.mp4")
        
        # Define target resolution
        target_width, target_height = 1080, 1350

        # Load and process the template image.
        if not os.path.exists(template_path):
            raise Exception(f"Template image not found at: {template_path}")
        template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template_img is None:
            raise Exception("Failed to load template image")
        template_img = cv2.resize(template_img, (target_width, target_height))
        if template_img.shape[2] == 4:
            template_img = cv2.cvtColor(template_img, cv2.COLOR_BGRA2BGR)

        # Open the input video.
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise Exception("Failed to open input video")
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = input_width / input_height
        print(f"Video loaded with FPS: {fps}, Resolution: {input_width}x{input_height}")

        # Calculate overlay dimensions while preserving aspect ratio.
        overlay_width = 920
        overlay_height = int(overlay_width / aspect_ratio)
        if overlay_width > target_width:
            overlay_width = target_width
            overlay_height = int(overlay_width / aspect_ratio)
        if overlay_height > target_height:
            overlay_height = target_height
            overlay_width = int(overlay_height * aspect_ratio)

        # Write the video using OpenCV to a temporary file.
        temp_output = os.path.join(output_dir, "temp_generated_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, fps, (target_width, target_height))
        print(f"Video creation started. Saving to temporary file: {temp_output}")

        frame_count = 0

        # Replace literal '\n' with actual newlines if they exist
        text_string = generate_caption(text_string)

                
        text_string = text_string.replace('\\n', '\n')
            # Split by actual newlines
        lines = text_string.split('\n')

        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Finished processing at frame count: {frame_count}")
                break
            # Resize the frame for overlay and prepare the result frame.
            overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
            result = template_img.copy()
            y1, y2 = video_pos[1], video_pos[1] + overlay_video.shape[0]
            x1, x2 = video_pos[0], video_pos[0] + overlay_video.shape[1]
            result[y1:y2, x1:x2] = overlay_video

            # Text handling exactly as in version 1
            # Define text position
            text_pos = (10, 900)
            
            # Split the text into multiple lines and handle newlines

            if text_string:
                y_offset = text_pos[1]
                for line in lines:
                    if line.strip():  # Only process non-empty lines
                        text_size = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)[0]
                        text_x = (target_width - text_size[0]) // 2
                        cv2.putText(result, line, (text_x, y_offset), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        y_offset += 40  # Adjust the offset for the next line

            out.write(result)
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")
        out.release()
        cap.release()
        cv2.destroyAllWindows()

        # Wait until the temporary file is stable (all data flushed).
        stable = False
        prev_size = -1
        while not stable:
            time.sleep(0.1)
            current_size = os.path.getsize(temp_output)
            if current_size == prev_size:
                stable = True
            prev_size = current_size
        print("Finished writing temporary video file.")

        # Re-encode the temporary video with FFmpeg to ensure proper streaming metadata.
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",                    # Overwrite output without prompt.
            "-i", temp_output,       # Input file.
            "-c:v", "libx264",       # Re-encode video to H.264.
            "-profile:v", "baseline",# Use baseline profile for compatibility.
            "-level", "3.0",
            "-pix_fmt", "yuv420p",   # Ensure compatibility.
            "-preset", "fast",
            "-crf", "22",            # Quality setting.
            "-movflags", "+faststart", # Move moov atom to the beginning.
            final_output             # Final output file.
        ]
        print("Running FFmpeg for re-encoding...")
        ffmpeg_result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ffmpeg_result.returncode != 0:
            err_msg = ffmpeg_result.stderr.decode()
            print("FFmpeg error:", err_msg)
            raise Exception("FFmpeg re-encoding failed: " + err_msg)
        # Remove the temporary file.
        os.remove(temp_output)
        print("Final video created at:", final_output)
        return final_output

    except Exception as e:
        print(f"An error occurred in create_templated_video: {str(e)}")
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()
        raise e

