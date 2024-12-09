


from TTS.api import TTS
import os

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)

def text_to_speech(text, output_file="output.wav"):
    tts.tts_to_file(text=text, file_path=output_file)

    if not os.path.exists(output_file):
        print(f"Error: {output_file} was not created!")

def generate_feedback_audio(feedback_text, output_file="feedback.wav"):
    """
    Converts feedback text into an audio file.
    """
    text_to_speech(feedback_text, output_file)
    return output_file
