import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the body parts and their 3D positions
body_parts_3d = {
    "head": (0, 0, 0),
    "neck": (0, 0, -10),
    "left_shoulder": (-10, 0, -10),
    "right_shoulder": (10, 0, -10),
    "left_elbow": (-20, 0, -20),
    "right_elbow": (20, 0, -20),
    "left_hand": (-30, 0, -30),
    "right_hand": (30, 0, -30),
    "torso": (0, 0, -20),
    "left_hip": (-10, 0, -40),
    "right_hip": (10, 0, -40),
    "left_knee": (-10, 0, -60),
    "right_knee": (10, 0, -60),
    "left_foot": (-10, 0, -80),
    "right_foot": (10, 0, -80)
}

# Define the bone connections
connections = [
    ("head", "neck"),
    ("neck", "left_shoulder"),
    ("neck", "right_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("right_shoulder", "right_elbow"),
    ("left_elbow", "left_hand"),
    ("right_elbow", "right_hand"),
    ("neck", "torso"),
    ("torso", "left_hip"),
    ("torso", "right_hip"),
    ("left_hip", "left_knee"),
    ("right_hip", "right_knee"),
    ("left_knee", "left_foot"),
    ("right_knee", "right_foot")
]

# Define the angle values based on your provided angles
angle_values = {
    "Angle between ankle, knee, and hip": (0, 0, -90),  # Adjust the Z-coordinate
    "Angle between hip, shoulder, and knee": (10, 0, -90),  # Adjust the Z-coordinate
    "Angle between shoulder, knee, and ankle": (-10, 0, -90)  # Adjust the Z-coordinate
}

# Plot the body parts
for part, (x, y, z) in body_parts_3d.items():
    ax.scatter(x, y, z, s=20, c='b')
    ax.text(x, y, z, part, ha='center', va='center')

# Plot the bone connections
for start_part, end_part in connections:
    start_x, start_y, start_z = body_parts_3d[start_part]
    end_x, end_y, end_z = body_parts_3d[end_part]
    ax.plot([start_x, end_x], [start_y, end_y], [start_z, end_z], 'b', linewidth=2)

# Annotate the plot with angle values
for angle, (x, y, z) in angle_values.items():
    ax.text(x, y, z, angle, ha='center', va='center')

# Set axis labels
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Show the 3D plot
plt.title("3D Human Skeleton with Angles")
plt.show()
