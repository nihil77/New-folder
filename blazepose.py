import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Define custom pose labels for Chen-style Tai Chi stances
POSE_LABELS = {
    "Bow Stance (Gongbu)": [mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE],
    "Horse Stance (Ma Bu)": [mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP],
    "Empty Stance (Xu Bu)": [mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.RIGHT_KNEE],
    "Tiger Stance (Hu Bu)": [mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE],
    # Add more custom labels and associated landmarks as needed
}

# Initialize stance tracking variables
current_stance = "Unknown"
start_time = time.time()
stance_duration = 0
min_stance_duration = 2  # Minimum duration to count as a stance (adjust as needed)

# Function to determine the pose label
def determine_pose_label(results):
    for label, landmarks in POSE_LABELS.items():
        is_match = all(results.pose_landmarks.landmark[landmark].visibility > 0.5 for landmark in landmarks)

        if is_match:
            return label

    return "Unknown"

# Function to detect and draw keypoints on the frame
def detect_pose(frame):
    global current_stance, start_time, stance_duration

    # Convert the frame to RGB format (MediaPipe requires RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform pose estimation on the frame
    results = pose.process(frame_rgb)

    # Check if landmarks are found
    if results.pose_landmarks is not None:
        # Draw skeleton lines connecting landmarks
        for connection in mp_pose.POSE_CONNECTIONS:
            start_point = connection[0]
            end_point = connection[1]
            start_x, start_y = int(results.pose_landmarks.landmark[start_point].x * frame.shape[1]), int(results.pose_landmarks.landmark[start_point].y * frame.shape[0])
            end_x, end_y = int(results.pose_landmarks.landmark[end_point].x * frame.shape[1]), int(results.pose_landmarks.landmark[end_point].y * frame.shape[0])
            cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        # Display landmark confidence scores
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            confidence = landmark.visibility  # Confidence score
            cv2.putText(frame, f"{idx}: {confidence:.2f}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Add pose label with modern font
        pose_label = determine_pose_label(results)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_color = (255, 255, 255)
        font_thickness = 2
        text_size = cv2.getTextSize(pose_label, font, font_scale, font_thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = frame.shape[0] - 10  # Display at the bottom
        cv2.putText(frame, pose_label, (text_x, text_y), font, font_scale, font_color, font_thickness)

        # Track stance duration
        if current_stance != pose_label:
            current_stance = pose_label
            start_time = time.time()
        else:
            stance_duration = time.time() - start_time

        # Display stance duration
        if stance_duration >= min_stance_duration:
            cv2.putText(frame, f"Stance: {current_stance} ({stance_duration:.1f}s)", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return frame

# Open a video capture stream from the webcam (use video source 0)
video_capture = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = video_capture.read()

    # Detect and draw pose landmarks on the frame
    frame_with_landmarks = detect_pose(frame)

    # Display the frame with landmarks in real-time
    cv2.imshow("Pose Landmarker", frame_with_landmarks)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
