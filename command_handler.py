# whisper_befehle/command_handler.py
from whisper_befehle.wetter_api import frage_wetter
from whisper_befehle.notizen import speichern, alle_anzeigen
from whisper_befehle.wiki import suche_wikipedia
from whisper_befehle.erinnerung import erstelle_timer
from whisper_befehle.netz import ist_online
from whisper_befehle.chatgpt_api import frage_chatgpt, frage_chatgpt_langfassung

def handle_command(text):
    text = text.lower()

    #  Netzprüfung
    online = ist_online()

    if "wie geht" in text:
        return "Mir geht es gut, danke der Nachfrage."

    elif "stopp chat" in text or "stop chat" in text or "stop" in text:
        return "Verstanden. Ich verabschiede mich."

    elif "hallo" in text or "hello" in text:
        return "Hallo! Wie kann ich dir helfen?"

    elif any(phrase in text for phrase in ["zeit", "uhr", "actual time", "current time", "give me the time", "what time"]):
        from datetime import datetime
        jetzt = datetime.now().strftime("%H:%M")
        print(f"Uhrzeit abgefragt: {jetzt}")
        return f"Es ist {jetzt} Uhr."

    elif "wetter" in text:
        if online:
            return frage_wetter("Luzern")
        else:
            return "Keine Internetverbindung – ich kann dir das Wetter gerade nicht sagen."

    elif "wikipedia" in text:
        if online:
            begriff = text.split("wikipedia")[-1].strip()
            return suche_wikipedia(begriff)
        else:
            return "Wikipedia braucht Internet – du bist aktuell offline."

    elif "erinnere mich in" in text:
        import re
        # Intelligente Zahlenwörter erkennen
        worte_zu_zahl = {
            "eine": 1, "einer": 1, "einem": 1,
            "zwei": 2, "drei": 3, "vier": 4, "fünf": 5
        }

        # Zahl oder Zahlwort suchen
        match = re.search(r"erinnere mich in (\d+|[a-zäöü]+) minuten?(?: an)? (.+)", text)
        if match:
            minuten_raw = match.group(1)
            nachricht = match.group(2).strip()

            try:
                minuten = int(minuten_raw)
            except ValueError:
                minuten = worte_zu_zahl.get(minuten_raw, None)

            if minuten is not None:
                return erstelle_timer(minuten, nachricht)

        return "Bitte gib die Erinnerung im Format an: 'Erinnere mich in X Minuten an Y'."

    elif "zeig mir meine notizen" in text or "was habe ich notiert" in text:
        return alle_anzeigen()

    elif "erzähl mir mehr" in text or "mach weiter" in text or "langfassung" in text:
        return frage_chatgpt_langfassung()

    else:
        if online:
            return frage_chatgpt(text)
        else:
            return "Du bist offline. Ich kann ohne Internet nur lokale Befehle ausführen."
