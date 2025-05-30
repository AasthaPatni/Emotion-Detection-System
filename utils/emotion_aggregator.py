
# emotion_aggregator.py

emotion_groups = {
    'positive': ['happy', 'calm', 'surprised'],
    'negative': ['sad', 'angry', 'fearful', 'disgust'],
    'neutral': ['neutral']
}

def get_emotion_group(emotion):
    for group, emotions in emotion_groups.items():
        if emotion in emotions:
            return group
    return 'unknown'

def aggregate_emotions(facial_emotion, speech_emotion):
    facial_group = get_emotion_group(facial_emotion)
    speech_group = get_emotion_group(speech_emotion)

    if facial_group == speech_group:
        return facial_emotion  # Or speech_emotion
    elif speech_group != 'unknown':
        return facial_emotion
    else:
        return  speech_emotion
