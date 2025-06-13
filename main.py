from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
import os

from DialogueManager import dialogue_manager_instance
from TtsService import generate_audio

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_responses")

@app.route("/api/dialog", methods=['POST'])
def handle_dialog():
    """
    Endpoint do obsługi dialogu z użytkownikiem.
    Przetwarza tekst od użytkownika i zwraca odpowiedź systemu.
    ---
    tags:
      - Dialog
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              example: "Chciałbym zagłosować"
    responses:
      200:
        description: Pomyślna odpowiedź systemu.
        schema:
          type: object
          properties:
            displayText:
              type: string
              example: "Na którego kandydata chcesz zagłosować?"
            audioUrl:
              type: string
              example: "http://localhost:5000/audio/response_123.wav"
      400:
        description: Błędne zapytanie (np. brak pola 'text').
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "The 'text' field is required in the request body."}), 400

    user_text = data.get('text')

    # Use the dialogue manager instance to get a response
    response_text = dialogue_manager_instance.process_message(user_text)

    # Generate audio for the response
    audio_url = generate_audio(response_text)

    if not audio_url:
        return jsonify({"error": "Failed to generate audio response."}), 500

    return jsonify({
        "displayText": response_text,
        "audioUrl": audio_url
    })

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    """Serves an audio file from the audio_responses directory."""
    print(f"Request to serve audio file: {filename}")
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)