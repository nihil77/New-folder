import cv2
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to check if the detected pose matches the Horse Stance criteria
def is_horse_stance(landmarks):
    # Define landmark indices for hips, knees, and ankles (adjust these based on the landmarks you want to use)
    left_hip = landmarks[11]
    right_hip = landmarks[12]
    left_knee = landmarks[23]
    right_knee = landmarks[24]
    left_ankle = landmarks[25]
    right_ankle = landmarks[26]

    # Define tolerance values for the acceptable range of positions
    hip_width_tolerance = 0.05
    knee_spacing_tolerance = 0.1

    # Check if the hips are approximately at the same horizontal level
    hips_are_level = abs(left_hip.x - right_hip.x) < hip_width_tolerance

    # Check if the knees are at a certain distance from each other
    knees_are_spaced = abs(left_knee.x - right_knee.x) > knee_spacing_tolerance

    # Check if the ankles are approximately at the same horizontal level
    ankles_are_level = abs(left_ankle.x - right_ankle.x) < hip_width_tolerance

    # Combine the criteria to determine if it's a Horse Stance
    is_horse_stance = hips_are_level and knees_are_spaced and ankles_are_level

    return is_horse_stance

# Open a webcam
cap = cv2.VideoCapture(0)

# Text for the skeletal guide
skeletal_guide = [
    "Horse Stance Guide:",
    "1. Stand with feet shoulder-width apart.",
    "2. Bend knees and lower body.",
    "3. Keep back straight and arms relaxed.",
    "4. Hold for 30s-1min, breathing deeply.",
    "5. Slowly straighten legs to exit.",
]

# Load the custom font
font_path = 'C:/Users/john/Downloads/fonts/Barlow/Barlow-Light.ttf'  # Path to Times New Roman font file
font = ImageFont.truetype(font_path, size=20)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        continue

    # Convert the frame to RGB format (MediaPipe Pose model expects RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to obtain pose landmarks
    results = pose.process(frame_rgb)

    # Check if any pose landmarks were detected
    if results.pose_landmarks is not None:
        landmarks = results.pose_landmarks.landmark

        # Check if the detected pose matches the Horse Stance criteria
        if is_horse_stance(landmarks):
            text_color = (0, 255, 0)  # Green text
            status_text = "Horse Stance Detected"
        else:
            text_color = (0, 0, 255)  # Red text
            status_text = "Not in Horse Stance"

        # Draw status text using Pillow
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        draw.text((10, 230), status_text, font=font, fill=text_color)

        # Convert the image back to OpenCV format
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Draw skeleton lines on the original frame
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Resize the frame
    frame = cv2.resize(frame, (1200, 600))

    # Display the skeletal guide with custom font and text color
    for i, text in enumerate(skeletal_guide):
        if is_horse_stance(landmarks):  # Change text color based on horse stance detection
            guide_text_color = (0, 255, 0)  # Green text
        else:
            guide_text_color = (0, 0, 255)  # Red text
        cv2.putText(frame, text, (20, 20 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, guide_text_color, 1)

    # Display the frame
    cv2.imshow("Horse Stance Detection", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
