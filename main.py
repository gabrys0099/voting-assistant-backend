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
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "The 'text' field is required in the request body."}), 400

    user_text = data.get('text')
    response_object = dialogue_manager_instance.process_message(user_text)
    response_text = response_object.get("text")
    response_data = response_object.get("data")
    audio_url = generate_audio(response_text)

    if not audio_url:
        return jsonify({"error": "Failed to generate audio response."}), 500

    return jsonify({
        "displayText": response_text,
        "audioUrl": audio_url,
        "payload": response_data
    })

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    print(f"Request to serve audio file: {filename}")
    return send_from_directory(AUDIO_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)