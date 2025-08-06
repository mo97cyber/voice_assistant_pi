# whisper_stt/modules/tts.py
# whisper_stt/modules/tts.py
import os
import time
import threading
import queue
from gtts import gTTS
from playsound import playsound
import pyttsx3
from whisper_befehle.netz import ist_online

# Warteschlange für Sprachausgaben
sprech_queue = queue.Queue()

def speak(text):
    sprech_queue.put(text)
    sprech_queue.join()  #  Warte, bis gesprochen wurde

# Hintergrund-Thread zur Sprachausgabe
def sprecher_thread():
    while True:
        text = sprech_queue.get()
        try:
            if ist_online():
                print(" TTS: Online-Modus (gTTS)")
                tts = gTTS(text=text, lang="de")
                filename = "tts_output.mp3"
                tts.save(filename)
                playsound(filename)
                os.remove(filename)
            else:
                print(" TTS: Offline-Modus (pyttsx3)")
                engine = pyttsx3.init()
                engine.setProperty('rate', 175)
                engine.setProperty('volume', 1.0)
                engine.say(text)
                engine.runAndWait()
        except Exception as e:
            print(" Fehler beim Abspielen:", e)
        sprech_queue.task_done()  #  Signal: "fertig gesprochen"

# Thread starten
threading.Thread(target=sprecher_thread, daemon=True).start()
