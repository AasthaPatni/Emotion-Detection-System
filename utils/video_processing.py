import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from tensorflow.keras.models import load_model
from app.utils.speech_emotion import predict_speech_emotion, model as speech_emotion_model
from app.utils.speech_data_preprocessor import extract_features

from app.utils.facial_emotion import detect_faces_and_emotions

from app.utils.emotion_aggregator import aggregate_emotions






# Load the pre-trained facial emotion model
emotion_model = load_model('facial_emotion_model/emotion_model.h5')  
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


def extract_and_predict(video_path):
    print("🔍 Starting emotion analysis for:", video_path)

    # Load video clip
    clip = VideoFileClip(video_path)

    # Step 1: Facial emotion detection
    print("🎞️ Extracting facial emotions...")
    facial_emotion = detect_faces_and_emotions(video_path)
    print("😐 Facial Emotion:", facial_emotion)

    # Step 2: Extract audio and save to a temporary path
    audio_path = "app/static/temp_audio.wav"
    if clip.audio is not None:
        clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
    else:
        print("⚠️ No audio track found in video.")
        audio_path = None

    # Step 3: Speech emotion detection
    speech_emotion = "not detected"
    if audio_path and os.path.exists(audio_path):
        print("🎙️ Extracting speech emotions...")
        features = extract_features(audio_path)
        if features is not None:
            speech_emotion = predict_speech_emotion(speech_emotion_model, features)
            print("🗣️ Speech Emotion:", speech_emotion)
        else:
            print("⚠️ Feature extraction failed, skipping speech emotion detection.")
    else:
        print("⚠️ Skipping speech emotion analysis due to missing audio.")

    # Step 4: Aggregated emotion
    final_emotion = aggregate_emotions(facial_emotion, speech_emotion)
    print("🧠 Final Aggregated Emotion:", final_emotion)

    return {
        "facial_emotion": facial_emotion,
        "speech_emotion": speech_emotion,
        "final_emotion": final_emotion
    }


def predict_emotion_from_image(image_path):
    print("🖼️ Predicting emotion from image:", image_path)

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        print("⚠️ No face detected in image.")
        return {"error": "No face detected"}

    # Process the first detected face
    x, y, w, h = faces[0]
    roi_gray = gray[y:y+h, x:x+w]
    roi_gray = cv2.resize(roi_gray, (48, 48))
    roi = roi_gray.astype('float32') / 255.0
    roi = np.expand_dims(roi, axis=0)
    roi = np.expand_dims(roi, axis=-1)

    prediction = emotion_model.predict(roi)[0]
    final_emotion = emotion_labels[np.argmax(prediction)]

    print("😊 Predicted Facial Emotion:", final_emotion)

    return {
        "facial_emotion": final_emotion,
        "speech_emotion": "N/A",
        "final_emotion": final_emotion
    }
