import mediapipe as mp
import cv2
import torch
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keypoint_rnn_model import KeypointRNN  # Import your PyTorch model

# Load your trained PyTorch model
input_size = 67  # Replace with your actual input size
hidden_size = 64  # Replace with your actual hidden size
num_layers = 1  # Replace with your actual number of layers
num_classes = 8  # Replace with your actual number of classes

model = KeypointRNN(input_size, hidden_size, num_layers, num_classes)
model.load_state_dict(torch.load("keypoint_rnn_model.pth"))
model.eval()

# Initialize LabelEncoder and fit it to your class labels
label_encoder = LabelEncoder()
label_encoder.classes_ = np.array(["Tame", "Bow-Arrow", "False Stance", "Four-Six", "Golden Rooster", "Horse Stance", "Sitting", "Taijiquan"])  # Replace with your actual class labels

# Initialize MediaPipe Hands module for keypoint extraction
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open a video capture stream
cap = cv2.VideoCapture(0)  # Use the appropriate video source (e.g., camera or video file)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Use MediaPipe to extract keypoints from the frame
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0].landmark  # Extract keypoints

            # Convert landmarks to a format suitable for your model
            keypoints = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks])

            # Preprocess keypoints (e.g., normalize and format as needed)
            # ...

            # Convert keypoints to a PyTorch tensor
            input_tensor = torch.Tensor(keypoints).view(1, 1, input_size)

            # Use your model to make predictions
            with torch.no_grad():
                output = model(input_tensor)
                _, predicted_class = torch.max(output, 1)
                stance = label_encoder.classes_[predicted_class.item()]

            # Draw the detected stance on the frame
            cv2.putText(frame, stance, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Stance Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
