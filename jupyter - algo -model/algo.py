import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

def calculate_angle(x1, y1, x2, y2, x3, y3):
    radians = math.acos((x1 * (x2 - x3) + y1 * (y2 - y3)) / (math.sqrt(x1**2 + y1**2) * (math.sqrt((x2 - x3)**2 + (y2 - y3)**2))))
    return math.degrees(radians) if (math.sqrt(x1**2 + y1**2) * math.sqrt((x2 - x3)**2 + (y2 - y3)**2)) > 0 else 0  # Avoid NaN for very small angles

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
        hip_width_tolerance = 5  # Tolerance for hip width
        knee_distance_tolerance = 5  # Tolerance for knee distance
        vertical_tolerance = 0.5  # Tolerance for vertical alignment (0.1, 0.2)

        # Check if the keypoints match criteria for Horse Stance
        is_correct_horse_stance = (
            abs(left_hip_x - right_hip_x) < hip_width_tolerance and
            abs(left_knee_x - right_knee_x) < knee_distance_tolerance and
            abs(left_knee_y - left_hip_y) < vertical_tolerance and
            abs(right_knee_y - right_hip_y) < vertical_tolerance
        )
    else:
        is_correct_horse_stance = False
        
    # Calculate angles
    angle_left_hip_knee = calculate_angle(
        landmarks[11].x, landmarks[11].y, landmarks[23].x, landmarks[23].y, landmarks[24].x, landmarks[24].y
    )

    angle_right_hip_knee = calculate_angle(
        landmarks[12].x, landmarks[12].y, landmarks[24].x, landmarks[24].y, landmarks[23].x, landmarks[23].y
    )

    return is_correct_horse_stance, angle_left_hip_knee, angle_right_hip_knee

# Open a webcam
cap = cv2.VideoCapture(0)

# Your guide for angle text
angle_guide = [
    "Horse Stance Angle:",
    "Left Hip-Knee Angle: {:.2f} degrees",
    "Right Hip-Knee Angle: {:.2f} degrees"
]

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
        is_correct_horse_stance, angle_left_hip_knee, angle_right_hip_knee = is_horse_stance_correct(landmarks)
        
        if is_correct_horse_stance:
            text_color = (0, 255, 0)  # Green text
            status_text = "Good: Stance for Horse Stance"
            skeleton_color = (0, 255, 0)  # Green lines
        else:
            text_color = (0, 0, 255)  # Red text
            status_text = "Bad: Stance for Horse Stance"
            skeleton_color = (0, 0, 255)  # Red lines

        # Draw skeleton lines on the original frame
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=skeleton_color, thickness=1, circle_radius=1),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=skeleton_color, thickness=1)
        )

        # Position for status text in the bottom-left corner
        text_x = 10
        text_y = frame.shape[0] - 20
        cv2.putText(frame, status_text, (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, text_color, 1)

        # Draw angle guide text
        for i, text in enumerate(angle_guide):  
            text = text.format(angle_left_hip_knee if i == 1 else angle_right_hip_knee)
            cv2.putText(frame, text, (10, 20 + 30 * i), cv2.FONT_HERSHEY_TRIPLEX, 0.5, text_color, 1)

    # Resize the frame
    frame = cv2.resize(frame, (1260, 600))  # width and height

    # Display the frame
    cv2.imshow("API", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
if cap is not None:
    cap.release()
cv2.destroyAllWindows()
