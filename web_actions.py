"""
Stateless, web-safe action handler. Implements the same user-facing commands as action.Action
but WITHOUT performing system-side effects (no webbrowser.open, no os.startfile, no shutdown/lock).
Returns a JSON-friendly dict with keys:
- text: string to speak/display
- open_url: optional URL the frontend may open
- shutdown: boolean (frontend may prompt/ignore)
"""
import text_to_speech
import datetime
import weather

try:
    import wikipedia
    _HAS_WIKIPEDIA = True
except Exception:
    _HAS_WIKIPEDIA = False


def handle_text(data):
    user_data = str(data).lower()
    weather_data = data

    # Name
    if "what is your name" in user_data:
        resp = "My name is Virtual Assistant"
        try:
            text_to_speech.text_to_speech(resp)
        except Exception:
            pass
        return {"text": resp}

    # Greetings
    if any(x in user_data for x in ["hello", "hi"]):
        resp = "Hi Sir, How can I help you?"
        try:
            text_to_speech.text_to_speech(resp)
        except Exception:
            pass
        return {"text": resp}

    if "good morning" in user_data:
        resp = "Good Morning Sir"
        try:
            text_to_speech.text_to_speech(resp)
        except Exception:
            pass
        return {"text": resp}

    if "good afternoon" in user_data:
        resp = "Good Afternoon Sir"
        try:
            text_to_speech.text_to_speech(resp)
        except Exception:
            pass
        return {"text": resp}

    if "good evening" in user_data:
        resp = "Good Evening Sir"
        try:
            text_to_speech.text_to_speech(resp)
        except Exception:
            pass
        return {"text": resp}

    # Wikipedia
    if "wikipedia" in user_data:
        if not _HAS_WIKIPEDIA:
            msg = "Wikipedia package not available on server."
            return {"text": msg}
        try:
            query = user_data.replace('wikipedia', '').strip()
            if not query:
                return {"text": "Please provide a topic for Wikipedia."}
            result = wikipedia.summary(query, sentences=3)
            try:
                text_to_speech.text_to_speech(result)
            except Exception:
                pass
            return {"text": result}
        except Exception:
            return {"text": "No Result Found"}

    # Time
    if "what is the time now" in user_data or user_data.strip() == "time" or " time" in user_data:
        current_time = datetime.datetime.now()
        Time = (str(current_time.hour) + " Hour " + str(current_time.minute) + " Minute")
        try:
            text_to_speech.text_to_speech(Time)
        except Exception:
            pass
        return {"text": Time}

    # Open sites (frontend should open URLs)
    if "open google" in user_data:
        return {"text": "Opening Google", "open_url": "https://www.google.com"}
    if "open youtube" in user_data:
        return {"text": "Opening YouTube", "open_url": "https://www.youtube.com"}
    if "open stackoverflow" in user_data:
        return {"text": "Opening StackOverflow", "open_url": "https://stackoverflow.com"}

    # Music
    if "play music" in user_data:
        return {"text": "Playing Music", "open_url": "https://gaana.com"}

    # Weather
    if "weather" in user_data:
        try:
            ans = weather.weather(weather_data)
        except Exception as e:
            ans = "Unable to fetch weather information: " + str(e)
        try:
            text_to_speech.text_to_speech(ans)
        except Exception:
            pass
        return {"text": ans}

    # PDF — return url or message
    if "pdf" in user_data:
        # Use settings.json if present
        import os, json
        settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
        pdf_path = ''
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    pdf_path = cfg.get('pdf_path', '') or ''
            except Exception:
                pdf_path = ''
        if not pdf_path:
            return {"text": "PDF path not configured. Update settings.json with pdf_path."}
        # If URL, return open_url
        if pdf_path.startswith('http://') or pdf_path.startswith('https://'):
            return {"text": "Opening PDF", "open_url": pdf_path}
        else:
            return {"text": "PDF path configured on server (local file)."}

    # Lock / Shutdown / Bye
    if "lock window" in user_data:
        return {"text": "Lock command received (not executed on server)."}
    if "shutdown" in user_data:
        return {"text": "ok sir", "shutdown": True}
    if "bye" in user_data:
        return {"text": "Good Bye"}

    # Default
    return {"text": "I am not able to understand"}
