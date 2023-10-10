import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

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

        # Draw skeleton lines on the original frame
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Resize the frame
    frame = cv2.resize(frame, (1200, 600))

    # Display the skeletal guide
    for i, text in enumerate(skeletal_guide):
        cv2.putText(frame, text, (20, 20 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("BlazePose Skeletal Guide", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
