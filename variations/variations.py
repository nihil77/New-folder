import pandas as pd
import numpy as np

data = {
    'label': ['Four-Six'],
    'x1': [156],
    'y1': [124],
    'x2': [160],
    'y2': [115],
    'x3': [162],
    'y3': [115],
    'x4': [165],
    'y4': [114],
    'x5': [151],
    'y5': [116],
    'x6': [148],
    'y6': [116],
    'x7': [145],
    'y7': [116],
    'x8': [170],
    'y8': [113],
    'x9': [140],
    'y9': [115],
    'x10': [161],
    'y10': [130],
    'x11': [151],
    'y11': [131],
    'x12': [196],
    'y12': [140],
    'x13': [118],
    'y13': [147],
    'x14': [222],
    'y14': [190],
    'x15': [81],
    'y15': [198],
    'x16': [241],
    'y16': [234],
    'x17': [49],
    'y17': [247],
    'x18': [250],
    'y18': [251],
    'x19': [36],
    'y19': [258],
    'x20': [241],
    'y20': [252],
    'x21': [39],
    'y21': [260],
    'x22': [238],
    'y22': [248],
    'x23': [47],
    'y23': [257],
    'x24': [193],
    'y24': [225],
    'x25': [148],
    'y25': [229],
    'x26': [251],
    'y26': [247],
    'x27': [133],
    'y27': [218],
    'x28': [330],
    'y28': [272],
    'x29': [147],
    'y29': [274],
    'x30': [335],
    'y30': [277],
    'x31': [155],
    'y31': [281],
    'x32': [353],
    'y32': [274],
    'x33': [130],
    'y33': [291]
}






# Number of variations to generate
num_variations = 29

# Output folder to save CSV files
output_folder = 'four_var'

# Create the output folder if it doesn't exist
import os
os.makedirs(output_folder, exist_ok=True)

# Create variations
for i in range(num_variations):
    variation = data.copy()
    for col in data:
        if col not in ['label']:
            # Add random perturbation to each coordinate
            variation[col] = [int(val + np.random.randint(-10, 8)) for val in data[col]]
    dataset = pd.DataFrame(variation)
    
    # Save the dataset to a CSV file
    filename = f'{output_folder}/landmark_dataset_{i+1}.csv'
    dataset.to_csv(filename, index=False)

print(f'{num_variations} datasets have been generated and saved to the "{output_folder}" folder.')
