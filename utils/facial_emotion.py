import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load model and label map once
facial_model = load_model("facial_emotion_model/emotion_model.h5")


emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

def detect_faces_and_emotions(video_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(video_path)

    emotions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray_frame[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, (48, 48))
            roi_normalized = roi_resized / 255.0
            roi_reshaped = np.reshape(roi_normalized, (1, 48, 48, 1))

            prediction = facial_model.predict(roi_reshaped, verbose=0)
            emotion_label = emotion_labels[np.argmax(prediction)]
            emotions.append(emotion_label)

    cap.release()
    cv2.destroyAllWindows()

    return max(set(emotions), key=emotions.count) if emotions else "No face detected"
