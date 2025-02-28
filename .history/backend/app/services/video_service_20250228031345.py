import cv2
import os
import time

# Determine the project root directory. Adjust this if your structure differs.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(100, 1150)):
    try:
        # Convert relative paths to absolute paths based on BASE_DIR
        input_video_path = os.path.join(BASE_DIR, input_video_path)
        output_path = os.path.join(BASE_DIR, output_path)
        template_path = os.path.join(BASE_DIR, template_path)

        # Define target resolution
        target_width, target_height = 1080, 1350

        # Ensure the template image exists and load it
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

        # Get input video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = input_width / input_height
        print(f"Video loaded with FPS: {fps}, Resolution: {input_width}x{input_height}")

        # Define overlay size while preserving the aspect ratio
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

        # Set up the video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))

        print(f"Video creation started. Saving to: {output_path}")

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Finished processing at frame count: {frame_count}")
                break

            # Resize the input frame for overlay
            overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
            result = template_img.copy()

            # Overlay the video frame onto the template image
            y1, y2 = video_pos[1], video_pos[1] + overlay_video.shape[0]
            x1, x2 = video_pos[0], video_pos[0] + overlay_video.shape[1]
            result[y1:y2, x1:x2] = overlay_video

            # Add text to the result
            cv2.putText(result, text_string, video_pos, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Write the processed frame to the output video
            out.write(result)
            frame_count += 1

            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")

        print(f"Video successfully created at: {output_path}")

        # Release resources to finalize the file
        out.release()
        cap.release()
        cv2.destroyAllWindows()

        # Wait until the output file size is stable
        stable = False
        prev_size = -1
        while not stable:
            time.sleep(0.1)
            current_size = os.path.getsize(output_path)
            if current_size == prev_size:
                stable = True
            prev_size = current_size

        print("Finished writing video to disk.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()
