

---

# 🎭 MoodLens

**MoodLens** is a multi-modal emotion detection system that leverages deep learning to analyze facial expressions, speech patterns, and behavioral trends. It provides real-time emotion recognition through a web-based interface and visualizes emotional patterns over time, making it ideal for research, mental health applications, and human-computer interaction projects.

---

## 📌 Description

MoodLens integrates computer vision, audio signal processing, and intelligent aggregation logic to detect and log human emotions. It uses pre-trained neural network models to classify emotions from images, videos, and audio recordings. The platform includes a Flask-based web dashboard for emotion tracking, trend visualization, and analysis.

---

## 🚀 Features

- 🧠 Facial emotion recognition using CNN models trained on FER-2013 dataset.
- 🎙️ Speech emotion classification using MFCC features and deep learning.
- 🎥 Multi-modal video/audio processing and real-time prediction.
- 📈 Trend visualization of emotional states over time.
- 💾 Upload interface for image, audio, and video files.
- 🛠 Model training, evaluation, and visualization tools included.

---

## 🗂️ Project Structure

```
MoodLens/
├── app/                          # Flask web app
│   ├── static/                   # Static assets (CSS, JS)
│   ├── templates/                # HTML templates (Jinja2)
│   └── __init__.py
│
├── utils/                        # Core logic for emotion detection
│   ├── facial_emotion.py
│   ├── speech_emotion.py
│   ├── emotion_aggregator.py
│   ├── emotion_logger.py
│   ├── mental_health_logic.py
│   ├── video_processing.py
│   └── test_predict.py
│
├── emotion_model/               # Facial emotion model
│   └── emotion_model.h5
│
├── uploads/                     # User-uploaded media files
├── speech_emotion_model.h5      # Trained speech emotion model
├── label_encoder.pkl            # Encoded class labels
├── confusion_matrix.png         # Model evaluation image
├── roc_curve.png                # ROC curve visualization
├── model_metrics_summary.csv    # Evaluation metrics summary
├── fer2013/                     # Facial emotion dataset (optional)
├── speech_emotion_dataset/      # Audio emotion dataset
├── train_emotion_model.py       # Script to train facial model
├── train_speech_model.py        # Script to train speech model
├── evaluate_model.py            # Evaluation logic
├── app.py                       # Entry point
└── requirements.txt             # Project dependencies
```

---

## 🛠️ Installation Instructions

1. **Clone the repository**
```bash
git clone https://github.com/your-username/MoodLens.git
cd MoodLens
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the required dependencies**
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Start

After installation, run the Flask app:

```bash
python app.py
```

Then visit: [http://localhost:5000](http://localhost:5000)

---

## 🧠 Emotion Detection Modules

### 🔹 Facial Emotion Recognition
- Uses Convolutional Neural Networks.
- Trained on FER-2013 dataset.
- Classes: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral.

### 🔹 Speech Emotion Detection
- Extracts MFCC features from audio.
- Uses a trained deep learning model (CNN/LSTM).

### 🔹 Video and Aggregated Emotion Analysis
- Processes both image and audio frames from uploaded video.
- Aggregates emotions detected from multiple sources to determine dominant mood.

### 🔹 Mental Health Logic Layer
- Tracks emotional trends.
- Flags prolonged negative states based on temporal data.

---

## 📊 Evaluation

- **Confusion Matrix**: `confusion_matrix.png`
- **ROC Curve**: `roc_curve.png`
- **Metrics Summary**: `model_metrics_summary.csv`
- **Accuracy and F1-scores**: Available via `evaluate_model.py`

---

## 📤 Upload Format

Upload any of the following file types to the `/uploads/` folder or through the web interface:

- 🎞 Video: `.mp4`, `.webm`
- 🎤 Audio: `.wav`
- 🖼 Images: `.jpeg`, `.jpg`, `.png`

---

## 🏷️ Emotion Classes

- 😀 Happy  
- 😢 Sad  
- 😠 Angry  
- 😨 Fear  
- 🤢 Disgust  
- 😲 Surprise  
- 😐 Neutral

---

## 📦 Dependencies

Install with:

```bash
pip install -r requirements.txt
```

Sample contents of `requirements.txt`:
```
tensorflow
keras
flask
numpy
pandas
opencv-python
matplotlib
scikit-learn
librosa
moviepy
```

---

## 💻 Technologies Used

- **Python 3.x**
- **TensorFlow & Keras** – Deep learning models
- **Flask** – Web framework
- **OpenCV** – Image/video processing
- **Librosa** – Audio feature extraction
- **MoviePy** – Video frame/audio handling
- **Scikit-learn** – Evaluation metrics & preprocessing
- **Matplotlib / Seaborn** – Data visualization

---



## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Added new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

---

