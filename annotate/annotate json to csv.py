import os
import csv
import json

# Define the directory containing your JSON annotation files
annotation_dir = 'C:/Users/john/OneDrive/Desktop/New folder/annotateimage'
# Define the output CSV file path
csv_file = "tai.csv"

# Initialize a CSV writer
with open(csv_file, mode="w", newline="") as csvfile:
    # Define the header with columns for label and keypoints (x, y)
    fieldnames = ["label"]
    for i in range(1, 34):
        fieldnames.extend([f"x{i}", f"y{i}"])  # Exclude "z" coordinates
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Iterate through JSON annotation files
    for filename in os.listdir(annotation_dir):
        if filename.endswith(".json"):
            annotation_file = os.path.join(annotation_dir, filename)
            
            # Load the JSON annotation
            with open(annotation_file, "r") as json_file:
                annotation_data = json.load(json_file)
            
            # Extract label from the image filename (assuming a specific naming convention)
            label = filename.split("_")[0]  # Modify as needed
            
            # Create a row for each keypoint (x, y)
            row = {"label": label}
            for i in range(1, 34):
                key = f"keypoint_{i}"
                row[f"x{i}"] = annotation_data[key]["x"]
                row[f"y{i}"] = annotation_data[key]["y"]
                
            # Write the row to the CSV file
            writer.writerow(row)

print(f"2D Keypoint dataset saved to {csv_file}")
