import cv2
import os

def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos, text_pos=(100, 1150)):
    try:
        # Define target resolution
        target_width, target_height = 1080, 1350

        # Load template image and resize to target resolution
        template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template_img is None:
            raise Exception("Failed to load template image")
        template_img = cv2.resize(template_img, (target_width, target_height))
        if template_img.shape[2] == 4:
            template_img = cv2.cvtColor(template_img, cv2.COLOR_BGRA2BGR)

        # Open input video
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise Exception("Failed to open input video")

        # Get input video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = input_width / input_height  # Lock this ratio

        # Define overlay size with locked aspect ratio
        overlay_width = 920  # Adjust this value (max 1080)
        overlay_height = int(overlay_width / aspect_ratio)  # Height scales with width

        # Ensure overlay fits within target resolution
        if overlay_width > target_width:
            overlay_width = target_width
            overlay_height = int(overlay_width / aspect_ratio)
        if overlay_height > target_height:
            overlay_height = target_height
            overlay_width = int(overlay_height * aspect_ratio)

        # Set up video writer
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Make sure the output directory exists
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize input frame with locked aspect ratio
            overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
            result = template_img.copy()

            # Overlay video onto template
            y1, y2 = video_pos[1], video_pos[1] + overlay_video.shape[0]
            x1, x2 = video_pos[0], video_pos[0] + overlay_video.shape[1]
            if y2 > target_height or x2 > target_width:
                print(f"Warning: Overlay exceeds bounds at {video_pos}. Cropping...")
                overlay_video = overlay_video[:target_height - video_pos[1], :target_width - video_pos[0]]
                y2 = target_height
                x2 = target_width
            result[y1:y2, x1:x2] = overlay_video

            # Add text
            cv2.putText(result, text_string, text_pos, 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Write frame
            out.write(result)

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(f"Video successfully created at: {output_path}")
        print(f"Overlay size: {overlay_width}x{overlay_height}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()
