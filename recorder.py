# whisper_stt/recorder.py

import sounddevice as sd
import scipy.io.wavfile as wav
import os

def record_to_wav(filename="whisper_stt/audio/aufnahme.wav", duration=5, samplerate=16000):
    print(f"🎙 Starte Aufnahme ({duration} Sekunden)...")
    aufnahme = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    # Ordner anlegen, falls nicht vorhanden
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Alte Datei löschen, wenn vorhanden
    if os.path.exists(filename):
        os.remove(filename)

    # Neue Datei speichern
    wav.write(filename, samplerate, aufnahme)
    print(f" Aufnahme gespeichert unter: {os.path.abspath(filename)}")
    print(" Aufnahme-Datei vorhanden?", os.path.exists(filename))

    return filename

# Testlauf
if __name__ == "__main__":
    record_to_wav()
