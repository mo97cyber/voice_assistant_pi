# whisper_befehle/notizen.py

import json
import os
from datetime import datetime

NOTIZ_DATEI = "notizen.json"

def speichern(text):
    notiz = {
        "zeit": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "inhalt": text
    }

    notizen = []
    if os.path.exists(NOTIZ_DATEI):
        with open(NOTIZ_DATEI, "r", encoding="utf-8") as f:
            notizen = json.load(f)

    notizen.append(notiz)

    with open(NOTIZ_DATEI, "w", encoding="utf-8") as f:
        json.dump(notizen, f, ensure_ascii=False, indent=2)

    return "Notiz gespeichert."

def alle_anzeigen():
    if not os.path.exists(NOTIZ_DATEI):
        return "Du hast noch keine Notizen."

    with open(NOTIZ_DATEI, "r", encoding="utf-8") as f:
        notizen = json.load(f)

    if not notizen:
        return "Du hast noch keine Notizen."

    antwort = "Hier sind deine Notizen:\n"
    for eintrag in notizen[-3:]:  # nur die letzten 3 anzeigen
        antwort += f"- ({eintrag['zeit']}) {eintrag['inhalt']}\n"
    return antwort
