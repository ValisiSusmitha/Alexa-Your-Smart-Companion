try:
    import speech_recognition as sr
    _HAS_SR = True
except Exception:
    _HAS_SR = False


def speech_to_text():
    """
    Capture voice from microphone and return transcribed text.
    If microphone or PyAudio is unavailable, fall back to console input.
    """
    if not _HAS_SR:
        # Fallback: ask user to type input in console
        try:
            return input("(SpeechRecognition not available) Type your input: ")
        except Exception:
            return ""

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
    except Exception as e:
        print("Microphone not available or failed:", e)
        # Fallback to console input
        try:
            return input("(Microphone not available) Type your input: ")
        except Exception:
            return ""

    try:
        voice_data = recognizer.recognize_google(audio)
        print("You said:", voice_data)
        return voice_data

    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
        return ""

    except sr.RequestError:
        print("Speech Recognition service is unavailable.")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""