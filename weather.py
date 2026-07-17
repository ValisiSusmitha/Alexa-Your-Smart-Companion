"""
Simple, reliable weather lookup using wttr.in (no API key required).
Falls back to a friendly message on network errors.
"""

import requests


def weather(var):
    # Extract location from command
    query = str(var).lower().replace("weather", "").strip()

    if query == "":
        query = "India"

    # Use wttr.in quick format: temperature and condition
    try:
        # wttr.in returns plain text for format; use '?format=j1' for JSON
        url = f"https://wttr.in/{requests.utils.quote(query)}?format=%t+%C"
        headers = {"User-Agent": "curl/7.64.1"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            text = resp.text.strip()
            # wttr.in returns temperature like +25°C or -3°C — preserve as-is
            return f"Weather for {query.title()}: {text}"
        else:
            return "Unable to fetch weather information. (status: {} )".format(resp.status_code)
    except Exception as e:
        return "Unable to fetch weather information: " + str(e)