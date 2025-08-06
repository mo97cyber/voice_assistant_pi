# whisper_befehle/wetter_api.py

import requests

# Deinen echten API-Key hier einfügen:
API_KEY = "Use_your_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def frage_wetter(stadt="Luzern", sprache="de"):
    params = {
        "q": stadt,
        "appid": API_KEY,
        "units": "metric",
        "lang": sprache
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        daten = response.json()

        if daten.get("cod") != 200:
            return f"Ich konnte das Wetter für {stadt} nicht finden."

        wetter = daten["weather"][0]["description"]
        temperatur = daten["main"]["temp"]
        return f"Das Wetter in {stadt}: {temperatur:.1f} Grad Celsius mit {wetter}."

    except Exception as e:
        return "Beim Abrufen des Wetters ist ein Fehler passiert."
