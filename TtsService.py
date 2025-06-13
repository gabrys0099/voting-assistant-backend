# tts_service.py
import pyttsx3
import os
import uuid

AUDIO_DIR = "audio_responses"


def generate_audio(text_to_read):
    """
    Generates an audio file from the given text and returns a URL to that file.
    """
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    try:
        engine = pyttsx3.init()

        file_name = f"response_{uuid.uuid4()}.wav"
        save_path = os.path.join(AUDIO_DIR, file_name)

        engine.save_to_file(text_to_read, save_path)
        engine.runAndWait()

        print(f"Generated audio file: {save_path}")
        file_url = f"/audio/{file_name}"
        return file_url

    except Exception as e:
        print(f"An error occurred during audio generation: {e}")
        return None