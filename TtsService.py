import os
import uuid
from TTS.api import TTS

MODEL_NAME = "tts_models/pl/mai_female/vits"
AUDIO_DIR = "audio_responses"
TTS_INSTANCE = None

def initialize_tts():
    global TTS_INSTANCE
    if TTS_INSTANCE is None:
        print("Inicjalizowanie modelu Coqui TTS... (może to chwilę potrwać przy pierwszym uruchomieniu)")
        try:
            TTS_INSTANCE = TTS(model_name=MODEL_NAME, gpu=False)
            print("Model TTS załadowany pomyślnie.")
        except Exception as e:
            print(f"KRYTYCZNY BŁĄD: Nie można załadować modelu TTS: {e}")
            print("Upewnij się, że masz połączenie z internetem przy pierwszym uruchomieniu.")
            exit()

def generate_audio(text_to_read):
    if TTS_INSTANCE is None:
        print("BŁĄD: Instancja TTS nie została zainicjalizowana.")
        return None

    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    try:
        file_name = f"response_{uuid.uuid4()}.wav"
        save_path = os.path.join(AUDIO_DIR, file_name)

        print(f"Generowanie audio dla tekstu: '{text_to_read}'")
        TTS_INSTANCE.tts_to_file(text=text_to_read, file_path=save_path)

        print(f"Wygenerowano plik audio: {save_path}")
        file_url = f"/audio/{file_name}"
        return file_url

    except Exception as e:
        print(f"Wystąpił błąd podczas generowania audio: {e}")
        return None

initialize_tts()