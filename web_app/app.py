from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import base64

# Optional Google Cloud clients
try:
    from google.cloud import speech
    from google.cloud import texttospeech
    _HAS_GOOGLE = True
except Exception:
    _HAS_GOOGLE = False

import web_actions

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Initialize Google clients if credentials are present
_google_speech_client = None
_google_tts_client = None
if _HAS_GOOGLE and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    try:
        _google_speech_client = speech.SpeechClient()
        _google_tts_client = texttospeech.TextToSpeechClient()
    except Exception:
        _google_speech_client = None
        _google_tts_client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/message', methods=['POST'])
def message():
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    response = web_actions.handle_text(text)
    return jsonify(response)

@app.route('/api/audio', methods=['POST'])
def audio_upload():
    # Accepts multipart/form-data with file field 'audio'
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    f = request.files['audio']
    audio_bytes = f.read()

    # Try Google Speech-to-Text
    if _google_speech_client:
        try:
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='en-US'
            )
            resp = _google_speech_client.recognize(config=config, audio=audio)
            transcripts = [r.alternatives[0].transcript for r in resp.results if r.alternatives]
            transcript = ' '.join(transcripts).strip()
            return jsonify({'transcript': transcript})
        except Exception as e:
            return jsonify({'error': 'Google STT failed: ' + str(e)}), 500
    else:
        return jsonify({'error': 'Server-side STT not configured. Set GOOGLE_APPLICATION_CREDENTIALS or use client-side speech.'}), 500

@app.route('/api/tts', methods=['POST'])
def tts():
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    if _google_tts_client:
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = _google_tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            audio_content = base64.b64encode(response.audio_content).decode('utf-8')
            return jsonify({'audio_base64': audio_content})
        except Exception as e:
            return jsonify({'error': 'Google TTS failed: ' + str(e)}), 500
    else:
        return jsonify({'error': 'Server-side TTS not configured. Set GOOGLE_APPLICATION_CREDENTIALS or use client-side speech.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
