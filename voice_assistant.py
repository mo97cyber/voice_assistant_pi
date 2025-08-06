# whisper_sprachassistent.py

from whisper_stt.recognizer import transcribe
from whisper_stt.recorder import record_to_wav
from whisper_befehle.command_handler import handle_command
from whisper_stt.modules.tts import speak
from whisper_befehle.netz import ist_online

import threading
import os
import re
import time

beenden_flag = False

# Wake-Wörter (mehrsprachig)
wakewords = ["start", "chat", "starte", "hallo", "bonjour", "hey", "aktivieren"]
stop_words = ["stopp chat", "stop chat", "stop", "tschüss", "ende", "ich bin fertig", "halt"]

letzte_aktivitaet = time.time()
timeout_dauer = 300  # 5 Minuten Inaktivität

def hauptloop():
    global beenden_flag, letzte_aktivitaet
    print("Chat hört zu. Sag etwas.")
    speak("Ich bin bereit.")
    time.sleep(3)

    while not beenden_flag:
        if time.time() - letzte_aktivitaet > timeout_dauer:
            print(" Inaktivität erkannt. Verabschiede mich.")
            speak("Ich war zu lange inaktiv. Ich verabschiede mich.")
            break

        speak("Sprich jetzt bitte.")
        time.sleep(2)

        record_to_wav()
        print("Aufnahme-Zeit:", os.path.getmtime("whisper_stt/audio/aufnahme.wav"))
        text = transcribe()
        print("Erkannt:", text)
        print("Debug (Whisper):", repr(text))

        if any(w in text.lower() for w in stop_words):
            print("Befehl erkannt: Beenden.")
            speak("Tschüss. Ich verabschiede mich.")
            break

        antwort = handle_command(text)
        print("Antwort:", antwort)
        speak(antwort)
        time.sleep(5)
        letzte_aktivitaet = time.time()

def main():
    global beenden_flag

    online_status = "online" if ist_online() else "offline"
    print(f" Netzwerkstatus: {online_status}")
    speak(f"Ich bin {online_status} und bereit. Sag etwas wie 'Start Chat', um loszulegen.")
    time.sleep(2)

    print("Warte auf Startbefehl wie 'Start Chat', 'Hey Chat', 'Bonjour Chat' ...")

    while not beenden_flag:
        speak("Ich höre. Sag bitte den Startbefehl.")
        time.sleep(3)

        record_to_wav()
        print("Aufnahme-Zeit:", os.path.getmtime("whisper_stt/audio/aufnahme.wav"))
        text = transcribe()
        print("Erkannt:", text)
        print("Debug (Whisper):", repr(text))

        worte = re.findall(r'\b\w+\b', text.lower())
        if any(w in worte for w in wakewords):
            print("Befehl erkannt: Wake Word wurde erkannt.")
            speak("Hallo. Wie kann ich dir helfen?")
            time.sleep(3)
            hauptloop()
            break

    print("Sprachassistent wurde beendet.")

if __name__ == "__main__":
    main()

