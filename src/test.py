import cv2
import mediapipe as mp
import numpy as np
import pickle
import pyttsx3

# 1. Load the Model
print("Loading model...")
model_dict = pickle.load(open('build/model.p', 'rb'))
model = model_dict['model']

# 2. Setup MediaPipe for 2 Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2, # We expect 126 features (21*3*2), so we need 2 hands
    min_detection_confidence=0.5)

# 3. Setup Text-to-Speech
engine = pyttsx3.init()
labels_dict = {
    0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four",
    5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"
}

# 4. Webcam Loop
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break
    
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    data_aux = []
    
    if results.multi_hand_landmarks:
        # We need to guarantee 126 features. 
        # If only 1 hand is visible, we must pad with zeros or the model crashes.
        
        # Collect all points
        x_ = []
        y_ = []
        
        # Iterate through detected hands (up to 2)
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
                data_aux.append(hand_landmarks.landmark[i].z) # Assuming Z is in your npy
                
                x_.append(x)
                y_.append(y)

            # Visual Feedback
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS)

        # CRITICAL FIX: The model expects exactly 126 features.
        # If the camera sees 1 hand (63 features), we pad the rest with zeros.
        required_length = 126
        current_length = len(data_aux)
        
        if current_length < required_length:
            data_aux.extend([0.0] * (required_length - current_length))
        elif current_length > required_length:
            data_aux = data_aux[:required_length]

        # Make Prediction
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]

        # Display Text
        cv2.rectangle(frame, (0, 0), (W, 60), (0, 0, 0), -1)
        cv2.putText(frame, predicted_character, (20, 45), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Optional: Speak (Warning: this might spam audio)
        # engine.say(predicted_character)
        # engine.runAndWait()

    cv2.imshow('Sign Language Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
