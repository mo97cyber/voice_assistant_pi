# whisper_befehle/chatgpt_api.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  #  Muss hier stehen


# OpenAI-Client initialisieren
last_prompt = None  # Globale Variable zum Speichern

def frage_chatgpt(prompt_text, kurzfassung=True):
    global last_prompt
    last_prompt = prompt_text  # merken für Langfassung

    try:
        system_msg = "Fasse dich sehr kurz (maximal 2 Sätze), antworte einfach und verständlich." if kurzfassung else "Gib eine ausführliche, vollständige Antwort."

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Sprachassistent."},
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt_text}
            ]
        )

        reply = response.choices[0].message.content.strip()
        # (Kostenanzeige bleibt gleich...)

        return reply

    except Exception as e:
        return f"Es gab ein Problem mit ChatGPT:\n\n{e}"

def frage_chatgpt_langfassung():
    global last_prompt
    if last_prompt:
        return frage_chatgpt(last_prompt, kurzfassung=False)
    else:
        return "Ich habe gerade nichts, worauf ich ausführlich antworten könnte."
