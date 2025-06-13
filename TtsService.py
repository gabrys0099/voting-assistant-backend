# tts_service.py
import pyttsx3
import os
import uuid

# Define the directory where audio files will be saved
AUDIO_DIR = "audio_responses"


def generate_audio(text_to_read):
    """
    Generates an audio file from the given text and returns a URL to that file.
    """
    # Ensure the directory for audio responses exists
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Generate a unique filename
        file_name = f"response_{uuid.uuid4()}.wav"
        save_path = os.path.join(AUDIO_DIR, file_name)

        # Save the speech to a file
        engine.save_to_file(text_to_read, save_path)

        # Run the engine to process the save_to_file command
        engine.runAndWait()

        print(f"Generated audio file: {save_path}")

        # Return the URL path that the frontend will use
        file_url = f"/audio/{file_name}"
        return file_url

    except Exception as e:
        print(f"An error occurred during audio generation: {e}")
        return None