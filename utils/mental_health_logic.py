# mental_health_logic.py

def analyze_trend(emotion):
    suggestions = {
        "happy": "Keep it up! Spread your positivity to others today 😊.",
        "sad": "Consider going for a walk, journaling your feelings, or listening to uplifting music 🎵.",
        "angry": "Try deep breathing, mindfulness, or short meditation sessions 🧘.",
        "fearful": "Talk to a friend or write down your thoughts to ease anxiety 🤝.",
        "surprised": "Channel your energy into something creative or reflective like art or journaling 🎨.",
        "disgusted": "Take a break and engage in something comforting like watching a favorite show or calling a loved one ☕📞.",
        "neutral": "Maintain balance and engage in light physical or creative activities to boost your mood 🧩.",
        "calm": "Enjoy the peace—perhaps take a few moments for gratitude or slow breathing 🌿."
    }

    emotion_tip = suggestions.get(emotion,"You can talk about your emotions with practice, even if it feels uncomfortable at first.")
    general_tip = "Take care of yourself and seek help if you're feeling overwhelmed. You're not alone ❤️."

    return {
        "emotion_tip": emotion_tip,
        "general_tip": general_tip
    }