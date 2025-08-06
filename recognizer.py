# whisper_stt/recognizer.py

from faster_whisper import WhisperModel
import os

def transcribe(audio_path="whisper_stt/audio/aufnahme.wav"):
    if not os.path.exists(audio_path):
        return " Datei nicht gefunden."

    model_size = "medium"
    model = WhisperModel(model_size, compute_type="auto")

    segments, _ = model.transcribe(audio_path)
    full_text = ""

    for segment in segments:
        full_text += segment.text + " "

    return full_text.strip()

# Testlauf
if __name__ == "__main__":
    print(" Ergebnis:", transcribe())
