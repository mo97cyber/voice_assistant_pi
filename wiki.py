# whisper_befehle/wiki.py
import wikipedia

# Optional: Deutsch als Standardsprache
wikipedia.set_lang("de")

def suche_wikipedia(begriff):
    try:
        zusammenfassung = wikipedia.summary(begriff, sentences=5)  # Begrenze auf 5 Sätze
        return zusammenfassung
    except wikipedia.exceptions.DisambiguationError as e:
        return f"'{begriff}' ist mehrdeutig. Bitte präzisieren. Vorschläge: {e.options[:3]}"
    except wikipedia.exceptions.PageError:
        return f"Ich habe zu '{begriff}' leider nichts gefunden."
    except Exception as e:
        return f"Wikipedia-Fehler: {e}"
