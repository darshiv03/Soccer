import cv2
import os
import uuid

# Determine the project root directory.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos, text_pos=(100,1150)):
    try:
        # Define target resolution
        target_width, target_height = 1080, 1350

        # Load template image and resize to target resolution
        template_path = os.path.join(BASE_DIR, template_path)
        template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template_img is None:
            raise Exception("Failed to load template image")
        template_img = cv2.resize(template_img, (target_width, target_height))
        if template_img.shape[2] == 4:
            template_img = cv2.cvtColor(template_img, cv2.COLOR_BGRA2BGR)

        # Open input video
        input_video_path = os.path.join(BASE_DIR, input_video_path)
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise Exception("Failed to open input video")

        # Get input video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = input_width / input_height  # Lock aspect ratio

        # Define overlay size with locked aspect ratio
        overlay_width = 920
        overlay_height = int(overlay_width / aspect_ratio)
        if overlay_width > target_width:
            overlay_width = target_width
            overlay_height = int(overlay_width / aspect_ratio)
        if overlay_height > target_height:
            overlay_height = target_height
            overlay_width = int(overlay_height * aspect_ratio)

        # Generate a unique final output filename
        output_dir = os.path.dirname(os.path.join(BASE_DIR, output_path))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        unique_id = uuid.uuid4().hex
        final_output = os.path.join(output_dir, f"generated_output_video_{unique_id}.mp4")

        # Set up video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(final_output, fourcc, fps, (target_width, target_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize input frame with locked aspect ratio
            overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
            result = template_img.copy()

            # Overlay video onto template at video_pos.
            y1, y2 = video_pos[1], video_pos[1] + overlay_video.shape[0]
            x1, x2 = video_pos[0], video_pos[0] + overlay_video.shape[1]
            if y2 > target_height or x2 > target_width:
                print(f"Warning: Overlay exceeds bounds at {video_pos}. Cropping...")
                overlay_video = overlay_video[:target_height - video_pos[1], :target_width - video_pos[0]]
                y2 = target_height
                x2 = target_width
            result[y1:y2, x1:x2] = overlay_video

            # Add caption text at text_pos.
            cv2.putText(result, text_string, text_pos, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            out.write(result)

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(f"Video successfully created at: {final_output}")
        return final_output

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()
        raise e

if __name__ == "__main__":
    # For local testing – adjust paths as needed.
    input_video = "/path/to/input_video.mp4"
    template_image = "/path/to/template.png"
    output_video = "/path/to/output_video.mp4"
    text_to_add = "Your Caption Here"
    create_templated_video(input_video, text_to_add, output_video, template_image, video_pos=(85,250))
