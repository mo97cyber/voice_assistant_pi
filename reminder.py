import time
import threading
from datetime import datetime, timedelta

aktive_timer = []

def erstelle_timer(minuten, nachricht):
    zielzeit = datetime.now() + timedelta(minutes=minuten)
    thread = threading.Thread(target=warte_und_melde, args=(zielzeit, nachricht))
    thread.daemon = True
    thread.start()
    aktive_timer.append((zielzeit, nachricht))
    return f"Ich erinnere dich in {minuten} Minuten daran: {nachricht}"

def warte_und_melde(zielzeit, nachricht):
    rest = (zielzeit - datetime.now()).total_seconds()
    if rest > 0:
        time.sleep(rest)
    from whisper_stt.modules.tts import speak
    speak(f"Erinnerung: {nachricht}")
    print(f" Erinnerung: {nachricht}")
