
from flask import Flask, request, render_template, jsonify, session
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import openai
import os
import speech_recognition as sr
from PIL import Image
import pytesseract

app = Flask(__name__)
app.secret_key = 'supersecretkey'

openai.api_key = os.getenv("OPENAI_API_KEY")

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_explanation', methods=['POST'])
def submit_explanation():
    # Handle text and audio inputs
    text = request.form.get('text')
    audio_file = request.files.get('audio')

    if not text or not audio_file:
        return jsonify({'error': 'Both text and audio explanation are required.'})

    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'explanation_audio.wav')
    audio_file.save(audio_path)

    try:
        audio = AudioSegment.from_file(audio_path)
        wav_path = os.path.splitext(audio_path)[0] + '.wav'
        audio.export(wav_path, format='wav')

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        user_explanation = recognizer.recognize_google(audio_data)
    except Exception as e:
        return jsonify({'error': f'Audio processing error: {str(e)}'})

    # Determine if it's the first or second attempt
    is_first_attempt = 'original_text' not in session

    if is_first_attempt:
        # Store the original text in the session
        session['original_text'] = text
        session['first_attempt'] = True

        # Generate a hint or partial feedback
        feedback = generate_feedback(user_explanation, session['original_text'], is_hint=True)
        return jsonify({'feedback': feedback, 'hint': True})
    else:
        # On second attempt, generate full feedback and clear session
        feedback = generate_feedback(user_explanation, session['original_text'], is_hint=False)
        session.clear()
        return jsonify({'feedback': feedback, 'hint': False})

# Generate feedback based on whether it's a hint or full feedback
def generate_feedback(user_explanation, original_text, is_hint):
    prompt = f"""
    You are a teacher giving feedback to a student. The student was asked to explain the following text:

    Original Text: {original_text}
    
    The student gave this explanation: {user_explanation}
    
    Now, provide feedback for the student, as if you were a teacher explaining to them why their explanation is correct or incorrect. 
    Please provide detailed feedback, pointing out where the explanation aligns or diverges from the original text, and offer helpful guidance for improvement.
    """

    if is_hint:
        prompt += "\nAlso, provide a short hint to guide the student in refining their answer without giving away the full explanation."
    else:
        prompt += "\nProvide a full, detailed feedback for the student about their explanation, including what they got right and what they missed."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content'].strip()

if __name__ == '__main__':
    app.run(debug=True)
