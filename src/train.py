import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle
import os

print("--- INITIALIZING ONE-SHOT TRAINING ---")

X_train = []
y_train = []

for i in range(11):
    filename = f"data/{i}.npy"
    if os.path.exists(filename):
        vector = np.load(filename)
        
        if vector.shape == (126,):
            vector = vector.reshape(1, -1)
            
        X_train.append(vector)
        y_train.append(i)
        print(f"Loaded {filename} as Class {i}")
    else:
        print(f"WARNING: {filename} missing!")

# Stack data into a matrix
# Final shape should be (11, 126)
X_train = np.vstack(X_train)
y_train = np.array(y_train)

# Initialize KNN with n_neighbors=1
# This means "Find the single closest matching example"
model = KNeighborsClassifier(n_neighbors=1)

# Fit the model
model.fit(X_train, y_train)

# Save the model artifact
with open('build/model.p', 'wb') as f:
    pickle.dump({'model': model}, f)

print("--- MISSION COMPLETE: model.p created ---")
