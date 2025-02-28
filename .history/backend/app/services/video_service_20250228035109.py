import cv2
import os
import time
import subprocess

# Determine the project root directory.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(100, 1150)):
    try:
        # Convert provided paths (relative to project root) to absolute paths
        input_video_path = os.path.join(BASE_DIR, input_video_path)
        output_path = os.path.join(BASE_DIR, output_path)
        template_path = os.path.join(BASE_DIR, template_path)

        # Define target resolution
        target_width, target_height = 1080, 1350

        # Load and process the template image
        if not os.path.exists(template_path):
            raise Exception(f"Template image not found at: {template_path}")
        template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template_img is None:
            raise Exception("Failed to load template image")
        template_img = cv2.resize(template_img, (target_width, target_height))
        if template_img.shape[2] == 4:
            template_img = cv2.cvtColor(template_img, cv2.COLOR_BGRA2BGR)

        # Open the input video
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise Exception("Failed to open input video")
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = input_width / input_height
        print(f"Video loaded with FPS: {fps}, Resolution: {input_width}x{input_height}")

        # Calculate overlay dimensions
        overlay_width = 920
        overlay_height = int(overlay_width / aspect_ratio)
        if overlay_width > target_width:
            overlay_width = target_width
            overlay_height = int(overlay_width / aspect_ratio)
        if overlay_height > target_height:
            overlay_height = target_height
            overlay_width = int(overlay_height * aspect_ratio)

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the video using OpenCV to a temporary file
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

            # Resize the frame for overlay and prepare the result frame
            overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
            result = template_img.copy()
            y1, y2 = video_pos[1], video_pos[1] + overlay_video.shape[0]
            x1, x2 = video_pos[0], video_pos[0] + overlay_video.shape[1]
            result[y1:y2, x1:x2] = overlay_video

            # Add text overlay
            cv2.putText(result, text_string, video_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            out.write(result)
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")

        out.release()
        cap.release()
        cv2.destroyAllWindows()

        # Wait until the temporary file is stable (ensuring all data is flushed)
        stable = False
        prev_size = -1
        while not stable:
            time.sleep(0.1)
            current_size = os.path.getsize(temp_output)
            if current_size == prev_size:
                stable = True
            prev_size = current_size
        print("Finished writing temporary video file.")

        # Before running FFmpeg, remove the final output file if it exists to avoid permission issues
        final_output = output_path
        if os.path.exists(final_output):
            os.remove(final_output)

        # Re-encode the temporary video with FFmpeg to repackage it (ensuring the moov atom is at the front)
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",                    # Overwrite output without prompt
            "-i", temp_output,       # Input file
            "-c:v", "libx264",       # Re-encode video to H.264
            "-profile:v", "baseline",# Use baseline profile for compatibility
            "-level", "3.0",
            "-pix_fmt", "yuv420p",   # Ensure compatibility
            "-preset", "fast",       # Encoding speed/quality tradeoff
            "-crf", "22",            # Quality setting
            "-movflags", "+faststart", # Move metadata to the front
            final_output             # Output file
        ]
        print("Running FFmpeg for re-encoding...")
        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("FFmpeg error:", result.stderr.decode())
            raise Exception("FFmpeg re-encoding failed.")
        os.remove(temp_output)
        print("Final video created at:", final_output)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()
