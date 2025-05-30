

import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
import pickle

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical

from app.utils.speech_data_preprocessor import extract_features

# Dataset path
dataset_path = 'speech_emotion_dataset'

# Emotion labels from RAVDESS
labels_map = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

features = []
labels = []

# Load and preprocess data
for root, _, files in os.walk(dataset_path):
    for file in files:
        if file.endswith('.wav'):
            parts = file.split('-')
            if len(parts) >= 3:
                emotion_code = parts[2]
                if emotion_code in labels_map:
                    label = labels_map[emotion_code]
                else:
                    continue
            else:
                continue

            file_path = os.path.join(root, file)
            try:
                feature = extract_features(file_path)
                features.append(feature)
                labels.append(label)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Convert to numpy arrays
X = np.array(features)

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
y = to_categorical(encoded_labels)

# Save the label encoder for inference
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# Check class distribution (for debugging)
from collections import Counter
print("Class distribution:", Counter(encoded_labels))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Optional: Use class weights to handle imbalance
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(encoded_labels),
    y=encoded_labels
)
class_weights = dict(enumerate(class_weights))

# Build the model
model = Sequential()
model.add(Dense(256, input_shape=(40,), activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(8, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model with class weights
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test),
          class_weight=class_weights)

# Save the model
model.save("speech_emotion_model.h5")
print("Model saved as speech_emotion_model.h5")
