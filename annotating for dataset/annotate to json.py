import cv2
import os
import json
import mediapipe as mp

# Load the MediaPipe BlazePose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define the folder containing your images
image_folder = 'C:/Users/john/Desktop/New folder/image_taijiquan'  # Replace 'your_image_folder' with your folder path

# Define the folder to save the JSON annotations
json_output_folder = 'annotateimage'  # Create this folder if it doesn't exist

# Ensure the output folder exists
os.makedirs(json_output_folder, exist_ok=True)

# Function to process an image, detect landmarks, and save annotations as JSON
def process_and_save_landmarks(image_path):
    # Load an image
    image = cv2.imread(image_path)

    # Convert the image to RGB format (MediaPipe BlazePose model expects RGB input)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to obtain pose landmarks
    results = pose.process(image_rgb)

    # Initialize a dictionary to store landmarks
    landmarks_dict = {}

    # Check if any landmarks were detected
    if results.pose_landmarks is not None:
        # Loop through the detected landmarks
        for landmark_id, landmark in enumerate(results.pose_landmarks.landmark):
            # Get the X and Y coordinates of the landmark (in pixel coordinates)
            image_height, image_width, _ = image.shape
            x, y = int(landmark.x * image_width), int(landmark.y * image_height)
            landmarks_dict[f"keypoint_{landmark_id+1}"] = {'x': x, 'y': y}

    # Save the landmarks as a JSON file
    json_file_path = os.path.join(json_output_folder, os.path.basename(image_path) + '.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(landmarks_dict, json_file)

# Iterate through images in the folder
for image_file in os.listdir(image_folder):
    if image_file.endswith(('.jpg', '.jpeg', '.png', '.JPG')):
        image_path = os.path.join(image_folder, image_file)
        process_and_save_landmarks(image_path)

print("2D Landmark annotation and JSON file creation complete.")
