import numpy as np

data = np.load('data/0.npy')

print(f"Data Type: {type(data)}")
print(f"Shape: {data.shape}") 
# Look for something like (NumberOfImages, Height, Width, Channels) 
# e.g., (1000, 64, 64, 3) for RGB or (1000, 64, 64) for Grayscale


# Output:
# Data Type: <class 'numpy.ndarray'>
# Shape: (126,)
# Note:
# We do not have raw images (pixels). We have Landmarks (Keypoints).
# 
#     The Math: Standard MediaPipe hand tracking extracts 21 points per hand. Each point has 3 coordinates (x, y, z).
# 
#         21 points × 3 coords = 63 values per hand.
# 
#         63 values × 2 hands = 126 values.
# 
#     The Implication: Our data pipeline has already processed the images and extracted the skeleton coordinates of the hands. This is actually good—training on coordinates is 100x faster and lighter than training on raw pixels (CNNs).
