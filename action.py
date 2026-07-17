import text_to_speech
import datetime
import webbrowser
import weather
try:
    import wikipedia
    _HAS_WIKIPEDIA = True
except Exception:
    _HAS_WIKIPEDIA = False
import os


def Action(data):

    user_data = str(data).lower()
    weather_data = data

    # ---------------- Name ---------------- #

    if "what is your name" in user_data:
        text_to_speech.text_to_speech("My name is Virtual Assistant")
        return "My name is Virtual Assistant"

    # ---------------- Greetings ---------------- #

    elif "hello" in user_data or "hi" in user_data:
        text_to_speech.text_to_speech("Hi Sir, How can I help you?")
        return "Hi Sir, How can I help you?"

    elif "good morning" in user_data:
        text_to_speech.text_to_speech("Good Morning Sir")
        return "Good Morning Sir"

    elif "good afternoon" in user_data:
        text_to_speech.text_to_speech("Good Afternoon Sir")
        return "Good Afternoon Sir"

    elif "good evening" in user_data:
        text_to_speech.text_to_speech("Good Evening Sir")
        return "Good Evening Sir"

    # ---------------- Wikipedia ---------------- #

    elif "wikipedia" in user_data:

        if not _HAS_WIKIPEDIA:
            msg = "Wikipedia package not available. Install 'wikipedia' to enable this feature."
            try:
                text_to_speech.text_to_speech(msg)
            except Exception:
                pass
            return msg

        try:

            text_to_speech.text_to_speech("Searching Wikipedia")

            user_data = user_data.replace("wikipedia", "")

            result = wikipedia.summary(user_data, sentences=3)

            text_to_speech.text_to_speech(result)

            return result

        except Exception:

            text_to_speech.text_to_speech("Sorry, I couldn't find anything.")

            return "No Result Found"

    # ---------------- Time ---------------- #

    elif "what is the time now" in user_data or "time" in user_data:

        current_time = datetime.datetime.now()

        Time = (
            str(current_time.hour)
            + " Hour "
            + str(current_time.minute)
            + " Minute"
        )

        text_to_speech.text_to_speech(Time)

        return Time

    # ---------------- Google ---------------- #

    elif "open google" in user_data:

        webbrowser.open("https://www.google.com")

        text_to_speech.text_to_speech("Google is now ready")

        return "Google Opened"

    # ---------------- YouTube ---------------- #

    elif "open youtube" in user_data:

        webbrowser.open("https://www.youtube.com")

        text_to_speech.text_to_speech("YouTube is now ready")

        return "YouTube Opened"

    # ---------------- StackOverflow ---------------- #

    elif "open stackoverflow" in user_data:

        webbrowser.open("https://stackoverflow.com")

        text_to_speech.text_to_speech("Stack Overflow is now ready")

        return "Stack Overflow Opened"

    # ---------------- Music ---------------- #

    elif "play music" in user_data:

        webbrowser.open("https://gaana.com")

        text_to_speech.text_to_speech("Gaana is now ready")

        return "Playing Music"

    # ---------------- Weather ---------------- #

    elif "weather" in user_data:

        try:
            ans = weather.weather(weather_data)
        except Exception as e:
            ans = "Unable to fetch weather information: " + str(e)

        try:
            text_to_speech.text_to_speech(ans)
        except Exception:
            pass

        return ans

    # ---------------- PDF ---------------- #

    elif "pdf" in user_data:

        try:

            # Try to read pdf path from settings.json in project root
            import json
            settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
            pdf_path = ""
            if os.path.exists(settings_path):
                try:
                    with open(settings_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                        pdf_path = cfg.get("pdf_path", "") or ""
                except Exception:
                    pdf_path = ""
            if not pdf_path:
                return "PDF path not configured. Create settings.json with {\"pdf_path\": \"C:\\\\path\\\\to\\\\file.pdf\"}"

            # If pdf_path looks like a URL, open in browser
            if pdf_path.startswith("http://") or pdf_path.startswith("https://"):
                try:
                    webbrowser.open(pdf_path)
                    return "Opening PDF in browser"
                except Exception as e:
                    return "Failed to open PDF URL: " + str(e)

            if not os.path.exists(pdf_path):
                return "PDF File Not Found: " + pdf_path
            try:
                os.startfile(pdf_path)
                return "Opening PDF"
            except Exception as e:
                return "Failed to open PDF: " + str(e)

        except Exception:

            return "PDF File Not Found"

    # ---------------- Lock Screen ---------------- #

    elif "lock window" in user_data:

        text_to_speech.text_to_speech("Locking the window")

        os.system("rundll32.exe user32.dll,LockWorkStation")

        return "Window Locked"

    # ---------------- Shutdown ---------------- #

    elif "shutdown" in user_data:

        text_to_speech.text_to_speech("Ok Sir")

        return "ok sir"

    # ---------------- Exit ---------------- #

    elif "bye" in user_data:

        text_to_speech.text_to_speech("Good Bye")

        return "Good Bye"

    # ---------------- Default ---------------- #

    else:

        text_to_speech.text_to_speech("I am not able to understand")

        return "I am not able to understand"