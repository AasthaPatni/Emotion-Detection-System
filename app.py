from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from app.utils.mental_health_logic import analyze_trend
from app.utils.video_processing import extract_and_predict, predict_emotion_from_image
import subprocess
import os
import json
from datetime import datetime
from collections import defaultdict

app = Flask(
    __name__,
    static_folder='app/static',
    template_folder='app/templates'
)

app.secret_key = 'your_secret_key_here'

# -------------------- CONFIG --------------------
UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = {'mp4', 'webm', 'avi', 'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------- HELPERS --------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_emotion_to_json(new_data, filename='app/static/emotion_log.json'):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "facial_emotion": new_data.get("facial_emotion"),
        "speech_emotion": new_data.get("speech_emotion"),
        "emotion": new_data.get("final_emotion")
    }

    data.append(entry)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# -------------------- ROUTES --------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['email'] == 'admin@example.com' and request.form['password'] == 'admin':
            session['user'] = request.form['email']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("index.html", result=None)
#------------------
def fix_webm_file(input_path, output_path):
    cmd = [
        r"C:\Users\apoor\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe",
        
        
        "-y","-i", input_path,
        "-c:v", "libvpx",
        "-c:a", "libvorbis",
        output_path
    ]
    subprocess.run(cmd, check=True)





    #-----uploads--------
from flask import Flask, render_template, request, redirect, url_for, session, flash

# Inside your upload route:
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'video_file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('index'))

    file = request.files['video_file']
    if file.filename == '':
        flash('No selected file.', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # If .webm, fix it
        if filename.endswith('.webm'):
            fixed_path = os.path.join(app.config['UPLOAD_FOLDER'], "webcam_recording_fixed.webm")
            fix_webm_file(filepath, fixed_path)
            filepath = fixed_path

        # Extract emotions
        result = extract_and_predict(filepath)

        if 'history' not in session:
            session['history'] = []
        session['history'].append(result['final_emotion'])
        session.modified = True

        suggestions = analyze_trend(result["final_emotion"])
        log_emotion_to_json(result)

        print("Sending to frontend:", result)
        print("Suggestion:", suggestions)

        return render_template('index.html', result=result, suggestion=suggestions)

    flash('Invalid file format.', 'error')
    return redirect(url_for('index'))
#--------------------------------------------------
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'image_file' not in request.files:
        return "No file part", 400

    file = request.files['image_file']
    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):  
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result = predict_emotion_from_image(filepath)

        if 'error' in result:
            return render_template("index.html", error=result["error"])

        # Save to history and log
        if 'history' not in session:
            session['history'] = []
        session['history'].append(result['final_emotion'])
        session.modified = True

        suggestions = analyze_trend(result["final_emotion"])
        log_emotion_to_json(result)

        return render_template("index.html", result=result, suggestion=suggestions)

    return "Invalid file format", 400


@app.route('/analysis')
def analysis():
    if 'user' not in session:
        return redirect(url_for('login'))

    log_path = os.path.join("app", "static", "emotion_log.json")
    if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
        return render_template('analysis.html', emotion_counts={})

    with open(log_path, 'r') as f:
        log_data = json.load(f)

    emotion_counts = defaultdict(int)
    for entry in log_data:
        emotion = entry["emotion"]
        emotion_counts[emotion] += 1

    return render_template('analysis.html', emotion_counts=dict(emotion_counts))

@app.route('/trends')
def trends():
    if 'user' not in session:
        return redirect(url_for('login'))

    log_path = os.path.join("app", "static", "emotion_log.json")
    if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
        return render_template('trends.html', trends={"Weekly": {}, "Monthly": {}})

    with open(log_path, 'r') as f:
        log_data = json.load(f)

    weekly_counts = defaultdict(int)
    monthly_counts = defaultdict(int)

    for entry in log_data:
        date = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        week = date.strftime("Week %W")
        month = date.strftime("%B")
        emotion = entry["emotion"]

        weekly_counts[f"{week} - {emotion}"] += 1
        monthly_counts[f"{month} - {emotion}"] += 1

    return render_template('trends.html', trends={
        "Weekly": dict(weekly_counts),
        "Monthly": dict(monthly_counts)
    })

@app.route('/reset_analysis')
def reset_analysis():
    log_file = "app/static/emotion_log.json"
    try:
        open(log_file, "w").close()
        return redirect(url_for('analysis'))
    except Exception as e:
        return f"<h3>❌ Failed to reset data: {str(e)}</h3>"

# -------------------- MAIN --------------------
if __name__ == '__main__':
    app.run(debug=True)
