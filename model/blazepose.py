import cv2
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

def is_horse_stance_correct(landmarks):
    keypoints_detected = (
        landmarks[11].visibility > 0.5 and  # Left hip
        landmarks[12].visibility > 0.5 and  # Right hip
        landmarks[23].visibility > 0.5 and  # Left knee
        landmarks[24].visibility > 0.5  # Right knee
    )

    if keypoints_detected:
        # Calculate distances
        left_hip_x = landmarks[11].x
        right_hip_x = landmarks[12].x
        left_knee_x = landmarks[23].x
        right_knee_x = landmarks[24].x

        left_hip_y = landmarks[11].y
        right_hip_y = landmarks[12].y
        left_knee_y = landmarks[23].y
        right_knee_y = landmarks[24].y

        # Tolerance values (you may need to adjust these)
        hip_width_tolerance = 0.5  # Tolerance for hip width
        knee_distance_tolerance = 1  # Tolerance for knee distance
        vertical_tolerance = 0.1  # Tolerance for vertical alignment (0.1, 0.2)

        # Check if the keypoints match criteria for Horse Stance
        is_correct_horse_stance = (
            abs(left_hip_x - right_hip_x) < hip_width_tolerance and
            abs(left_knee_x - right_knee_x) < knee_distance_tolerance and
            abs(left_knee_y - left_hip_y) < vertical_tolerance and
            abs(right_knee_y - right_hip_y) < vertical_tolerance
        )
    else:
        is_correct_horse_stance = False

    return is_correct_horse_stance


# Open a webcam
cap = cv2.VideoCapture(0)

# Text for the skeletal guide
skeletal_guide = [
    "Get ready to perform the Horse Stance:",
    "1. Stand with feet shoulder-width apart.",
    "2. Bend knees and lower body.",
    "3. Keep back straight and arms relaxed.",
    "4. Hold for 30s-1min, breathing deeply.",
    "5. Slowly straighten legs to exit.",
]

# Load the custom font
font_path = 'model/Barlow-Light.ttf'  # Path to font file
font = ImageFont.truetype(font_path, size=26)

while cap is not None and cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read a frame from the webcam.")
        break

    # Convert the frame to RGB format (MediaPipe Pose model expects RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to obtain pose landmarks
    results = pose.process(frame_rgb)

    # Check if any pose landmarks were detected
    if results.pose_landmarks is not None:
        landmarks = results.pose_landmarks.landmark

        # Check if the detected pose matches the Horse Stance
        is_correct_horse_stance = is_horse_stance_correct(landmarks)
        
        if is_correct_horse_stance:
            text_color = (0, 255, 0)  # Green text
            status_text = "Horse Stance Detected"
            skeleton_color = (0, 255, 0)  # Green lines
        else:
            text_color = (0, 0, 255)  # Red text
            status_text = "Not in Horse Stance"
            skeleton_color = (0, 0, 255)  # Red lines

        # Draw status text using Pillow
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        draw.text((370, 20), status_text, font=font, fill=text_color)

        # Convert the image back to OpenCV format
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Draw skeleton lines on the original frame with the selected color
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=skeleton_color, thickness=1, circle_radius=1),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=skeleton_color, thickness=1)
        )

        # Display the skeletal guide with custom font and text color
        for i, text in enumerate(skeletal_guide):
          if is_correct_horse_stance:
            guide_text_color = (0, 255, 0)  # Green text
          else:
            guide_text_color = (0, 0, 255)  # Red text

            cv2.putText(frame, text, (20, 20 + 30 * i), cv2.FONT_HERSHEY_TRIPLEX, 0.5, guide_text_color, 1)

    # Resize the frame
    frame = cv2.resize(frame, (1300, 800))  

    # Display the frame
    cv2.imshow("8 Foundational Taijiquan Stances", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
if cap is not None:
    cap.release()
cv2.destroyAllWindows()
