import numpy as np
import pickle
from keras.models import load_model
from .speech_data_preprocessor import extract_features

# Load model and label encoder
model = load_model("speech_emotion_model.h5")
with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

def predict_speech_emotion(model, features):
    features = np.array(features).reshape(1, 40)  # force shape (1, 40)
    if features.shape[1] != 40:
        raise ValueError(f"Expected feature shape (1, 40), but got {features.shape}")
    
    prediction = model.predict(features)
    pred_index = np.argmax(prediction)
    emotion = le.inverse_transform([pred_index])[0]
    return emotion

