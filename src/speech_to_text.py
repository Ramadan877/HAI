

import whisper

model = whisper.load_model("small")

def speech_to_text(audio_file_path):
    """
    Convert audio to text using Whisper.
    """
    result = model.transcribe(audio_file_path)
    return result["text"]
