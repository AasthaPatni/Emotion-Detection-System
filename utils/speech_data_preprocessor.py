import librosa
import numpy as np

def extract_features(file_path):
    try:
        # Load 2.5 seconds of audio from 0.6 seconds offset to avoid silence
        audio, sample_rate = librosa.load(file_path, duration=2.5, offset=0.6)
        # Extract 40 MFCCs (Mel Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        # Take mean over time (across all frames) to get a 40-dimensional feature
        mfccs_mean = np.mean(mfccs.T, axis=0)
        return mfccs_mean  # Shape: (40,)
    except Exception as e:
        print(f"❌ Error extracting features: {e}")
        return None
