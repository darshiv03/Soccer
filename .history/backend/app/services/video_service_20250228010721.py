# import os
# import cv2

# def create_templated_video(input_video_path, text_string, output_path, template_path, video_pos=(100, 1150)):
#     try:
#         # Define target resolution
#         target_width, target_height = 1080, 1350

#         # Ensure the template path is correct
#         if not os.path.exists(template_path):
#             raise Exception(f"Template image not found at: {template_path}")

#         # Load template image and resize to target resolution
#         template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
#         if template_img is None:
#             raise Exception("Failed to load template image")
#         template_img = cv2.resize(template_img, (target_width, target_height))
#         if template_img.shape[2] == 4:
#             template_img = cv2.cvtColor(template_img, cv2.COLOR_BGRA2BGR)

#         # Open input video
#         cap = cv2.VideoCapture(input_video_path)
#         if not cap.isOpened():
#             raise Exception("Failed to open input video")

#         # Get input video properties
#         fps = int(cap.get(cv2.CAP_PROP_FPS))
#         input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         aspect_ratio = input_width / input_height

#         # Define overlay size with locked aspect ratio
#         overlay_width = 920
#         overlay_height = int(overlay_width / aspect_ratio)

#         # Ensure overlay fits within target resolution
#         if overlay_width > target_width:
#             overlay_width = target_width
#             overlay_height = int(overlay_width / aspect_ratio)
#         if overlay_height > target_height:
#             overlay_height = target_height
#             overlay_width = int(overlay_height * aspect_ratio)

#         # Ensure the output directory exists
#         output_dir = os.path.dirname(output_path)
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)  # Create the directory if it doesn't exist

#         # Set up video writer
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Resize input frame with locked aspect ratio
#             overlay_video = cv2.resize(frame, (overlay_width, overlay_height))
#             result = template_img.copy()

#             # Overlay video onto template
#             y1, y2 = video_pos[1], video_pos[1] + overlay_video.shape[0]
#             x1, x2 = video_pos[0], video_pos[0] + overlay_video.shape[1]
#             result[y1:y2, x1:x2] = overlay_video

#             # Add text
#             cv2.putText(result, text_string, video_pos, 
#                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

#             # Write frame
#             out.write(result)

#         cap.release()
#         out.release()
#         cv2.destroyAllWindows()

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         if 'cap' in locals():
#             cap.release()
#         if 'out' in locals():
#             out.release()
#         cv2.destroyAllWindows()

# app/services/video_service.py


##########################################################################

# New version
# import shutil

# def process_video(input_video_path: str, output_video_path: str):
#     # Placeholder function for video processing.
#     # Just copy the input video to output for now
#     shutil.copy(input_video_path, output_video_path)

##########################################################################

import cv2
import os
import shutil

def process_video(input_video_path: str, output_video_path: str, template_path: str, text_string: str, video_pos=(100, 1150)):
    try:
        # Ensure the template path is correct
        if not os.path.exists(template_path):
            raise Exception(f"Template image not found at: {template_path}")

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_video_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define target resolution (same resolution as input video for simplicity)
        cap = cv2.VideoCapture(input_video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        target_width = input_width
        target_height = input_height

        # Load template image and resize to the same resolution as the input video
        template_img = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template_img is None:
            raise Exception("Failed to load template image")
        template_img = cv2.resize(template_img, (target_width, target_height))

        # Set up video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (target_width, target_height))

        # Process the video frame by frame
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Apply the template overlay onto the video frame (the overlay should be blended)
            result = frame.copy()
            # Assuming the template image is an overlay (for simplicity, just replacing the entire frame)
            result = template_img  # Replacing the frame with template for now

            # Add text overlay to the frame
            cv2.putText(result, text_string, video_pos, 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Write the frame to the output video
            out.write(result)

        cap.release()
        out.release()

        cv2.destroyAllWindows()
        print(f"Processed video saved at: {output_video_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()
        cv2.destroyAllWindows()



