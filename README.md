Alexa - Your Smart Companion (Desktop + Web)

Overview

This repository contains two variants of the same assistant:
- Desktop Tkinter app (original) — stays for local usage and quick testing
- Web app (Flask) — modern web interface with optional Google Cloud Speech-to-Text and Text-to-Speech support (server-side)

Security note
- Never commit or paste Google service account JSON into the repo or chat. Instead set GOOGLE_APPLICATION_CREDENTIALS on your server to point to the JSON file location.

Quick setup (development)
1. Create & activate venv (PowerShell):
   cd "C:\\Users\\Valisi Susmitha\\OneDrive\\Documents\\Desktop\\Alexa-Your-Smart-Companion"
   python -m venv .\\venv
   .\\venv\\Scripts\\Activate.ps1

2. Install dependencies:
   python -m pip install --upgrade pip
   pip install -r requirements.txt

3. (Optional) Configure Google Cloud credentials for server-side STT/TTS:
   - Create a Google Cloud service account with Speech-to-Text and Text-to-Speech roles.
   - Download the JSON key file and set an environment variable on the server:
     $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\\path\\to\\service-account.json"

4. Run the web app:
   .\\venv\\Scripts\\python -m web_app.app

5. Open your browser to http://localhost:5000

Features implemented in web app
- Typed and voice input (browser mic; uploads audio to server for STT when Google credentials are configured)
- Wikipedia lookup (server-side, if package available)
- Weather lookup (wttr.in, no API key required)
- Open common websites (frontend opens URLs provided by server)
- PDF handling (opens configured URL)
- Server-side TTS with Google Cloud TTS; falls back to browser speechSynthesis if not configured

Notes about speech
- Server-side STT/TTS requires GOOGLE_APPLICATION_CREDENTIALS set on the host. If not set, the web app will return an error for server-side STT/TTS endpoints — the frontend will still be able to use the browser's Web Speech API and speechSynthesis for client-side operation.

Next steps I can take
- Stream audio to Google STT incrementally for lower latency
- Replace wttr.in with OpenWeatherMap (requires API key)
- Add Dockerfile and systemd service example for deploying the Flask app

