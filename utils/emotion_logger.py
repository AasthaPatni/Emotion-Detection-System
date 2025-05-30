# app/utils/emotion_logger.py

import os
import json
from datetime import datetime

LOG_FILE = os.path.join("data", "emotion_logs.json")

def log_emotion_to_json(result):
    os.makedirs("data", exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "facial_emotion": result.get("facial_emotion", ""),
        "speech_emotion": result.get("speech_emotion", ""),
        "final_emotion": result.get("final_emotion", "")
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)
