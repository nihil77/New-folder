import cv2
import mediapipe as mp
import math

def calculate_angle(keypoints, keypoint_1, keypoint_2, keypoint_3):
    point1 = keypoints[keypoint_1]
    point2 = keypoints[keypoint_2]
    point3 = keypoints[keypoint_3]

    # Calculate the vectors ba and bc
    ba = [point1[0] - point2[0], point1[1] - point2[1]]
    bc = [point3[0] - point2[0], point3[1] - point2[1]]

    # Calculate the cosine of the angle between ba and bc
    cosine_angle = (ba[0] * bc[0] + ba[1] * bc[1]) / (math.sqrt(ba[0]**2 + ba[1]**2) * math.sqrt(bc[0]**2 + bc[1]**2))

    # Calculate the angle in degrees
    angle = math.degrees(math.acos(cosine_angle))

    return angle

# Load the image
image = cv2.imread("C:/Users/john/OneDrive/Desktop/New folder/image_taijiquan/Horse stance 2.jpg")

# Initialize the MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Convert the image to RGB format
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run inference on the image
results = pose.process(image_rgb)

# Extract keypoints
if results.pose_landmarks:
    keypoints = [(landmark.x, landmark.y) for landmark in results.pose_landmarks.landmark]

    # Calculate angles
    angle_1 = calculate_angle(keypoints, 0, 1, 2)
    angle_2 = calculate_angle(keypoints, 1, 2, 3)
    angle_3 = calculate_angle(keypoints, 2, 3, 4)

    # Print the angles
    print(f"Angle 1: {angle_1} degrees")
    print(f"Angle 2: {angle_2} degrees")
    print(f"Angle 3: {angle_3} degrees")

    # Display the image with keypoints (for visualization)
    for i, (x, y) in enumerate(keypoints):
        cv2.circle(image, (int(x * image.shape[1]), int(y * image.shape[0])), 5, (0, 0, 255), -1)
        cv2.putText(image, str(i), (int(x * image.shape[1]), int(y * image.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Pose Estimation", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
