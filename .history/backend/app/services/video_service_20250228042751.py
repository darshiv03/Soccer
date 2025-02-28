import cv2
import os
import time
import subprocess
import uuid

# Determine the project root directory.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(85, 250)):
    try:
        # Convert provided paths (relative to project root) to absolute paths.
        input_video_path = os.path.join(BASE_DIR, input_video_path)
        template_path = os.path.join(BASE_DIR, template_path)
        
        # Prepare the output directory and generate a unique final filename.
        output_dir = os.path.dirname(os.path.join(BASE_DIR, output_path))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        unique_id = uuid.uuid4().hex
        final_output = os.path.join(output_dir, f"generated_output_video_{unique_id}.mp4")
        
        # Reduced target resolution.
        target_width, target_height = 720, 900

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

        # Write video using OpenCV to a temporary file.
        temp_output = os.path.join(output_dir, "temp_generated_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, fps, (target_width, target_height))
        print(f"Video creation started. Saving to temporary file: {temp_output}")

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Finished processing at frame count: {frame_count}")
                break

            # Resize the frame for overlay.
            overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
            
            # Adjust the overlay position if it would extend out-of-bound.
            video_pos_x, video_pos_y = video_pos
            if video_pos_x + overlay_video.shape[1] > target_width:
                video_pos_x = (target_width - overlay_video.shape[1]) // 2
            if video_pos_y + overlay_video.shape[0] > target_height:
                video_pos_y = (target_height - overlay_video.shape[0]) // 2

            # Define the region where the overlay will be placed.
            y1, y2 = video_pos_y, video_pos_y + overlay_video.shape[0]
            x1, x2 = video_pos_x, video_pos_x + overlay_video.shape[1]

            # Start with a fresh copy of the template.
            result = template_img.copy()
            result[y1:y2, x1:x2] = overlay_video

            # Add overlay text (e.g. instructions) at the specified video position.
            cv2.putText(result, text_string, (video_pos_x, video_pos_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Add a caption at the bottom center of the frame.
            caption_text = text_string  # You can change this if you wish.
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            (text_width, text_height), baseline = cv2.getTextSize(caption_text, font, font_scale, thickness)
            caption_x = (target_width - text_width) // 2
            caption_y = target_height - 30  # 30 pixels above the bottom.
            cv2.putText(result, caption_text, (caption_x, caption_y), font, font_scale, (255,255,255), thickness, cv2.LINE_AA)

            out.write(result)
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")
                
        out.release()
        cap.release()
        cv2.destroyAllWindows()

        # Wait until the temporary file is stable.
        stable = False
        prev_size = -1
        while not stable:
            time.sleep(0.1)
            current_size = os.path.getsize(temp_output)
            if current_size == prev_size:
                stable = True
            prev_size = current_size
        print("Finished writing temporary video file.")

        # Re-encode with FFmpeg to ensure streaming compatibility.
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i", temp_output,
            "-c:v", "libx264",
            "-profile:v", "baseline",
            "-level", "3.0",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-crf", "22",
            "-movflags", "+faststart",
            final_output
        ]
        print("Running FFmpeg for re-encoding...")
        ffmpeg_result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ffmpeg_result.returncode != 0:
            err_msg = ffmpeg_result.stderr.decode()
            print("FFmpeg error:", err_msg)
            raise Exception("FFmpeg re-encoding failed: " + err_msg)
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
