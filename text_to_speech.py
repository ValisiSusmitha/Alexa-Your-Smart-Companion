try:
    import pyttsx3
    _TTS_AVAILABLE = True
except Exception:
    _TTS_AVAILABLE = False

engine = None
if _TTS_AVAILABLE:
    try:
        engine = pyttsx3.init()
        # Set speech rate
        try:
            engine.setProperty("rate", 170)
        except Exception:
            pass
        # Set voice to first available
        try:
            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)
        except Exception:
            pass
    except Exception:
        engine = None
        _TTS_AVAILABLE = False


def text_to_speech(text):
    """
    Converts text into speech if pyttsx3 is available, otherwise prints.
    """
    try:
        if _TTS_AVAILABLE and engine is not None:
            try:
                engine.say(text)
                engine.runAndWait()
            except RuntimeError:
                # If the speech engine has a busy loop, fall back to console output.
                print("TTS:", text)
            except Exception as e:
                print("TTS failed:", e)
                print(text)
        else:
            print("TTS:", text)
    except Exception as e:
        print("TTS failed:", e)
        print(text)
