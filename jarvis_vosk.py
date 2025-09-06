# jarvis_vosk.py
import os
import sys
import json
import queue
import webbrowser
import subprocess
import sounddevice as sd
import vosk
import pyttsx3
import openai
from dotenv import load_dotenv

# -------------------------
# Setup API key
# -------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in .env")
openai.api_key = OPENAI_API_KEY

# -------------------------
# Setup TTS (pyttsx3)
# -------------------------
tts = pyttsx3.init()
tts.setProperty("rate", 180)

def speak(text: str):
    print("JARVIS:", text)
    tts.say(text)
    tts.runAndWait()

# -------------------------
# Setup VOSK STT
# -------------------------
MODEL_PATH = "vosk-model-small-en-us-0.15"  # make sure this folder exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Download the VOSK model and place it in this folder.")

model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen_vosk():
    """Listen to mic input and return recognized text (offline)."""
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        print("Listening...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("You:", text)
                    return text

# -------------------------
# Local Actions
# -------------------------
def handle_open_website(query: str):
    if not query.startswith("http"):
        url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    else:
        url = query
    webbrowser.open(url)
    speak(f"Opening {query}")

def handle_run_command(cmd: str):
    try:
        subprocess.Popen(cmd, shell=True)
        speak(f"Running {cmd}")
    except Exception as e:
        speak(f"Failed to run command: {e}")

# -------------------------
# Ask OpenAI
# -------------------------
def ask_openai(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # change if needed
            messages=[
                {"role": "system", "content": "You are JARVIS, a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI API error:", e)
        return "Sorry, I couldn't connect to the AI service."

# -------------------------
# Main Loop
# -------------------------
def main():
    speak("Jarvis online. Say 'exit' or 'stop' to quit.")
    while True:
        text = listen_vosk()
        if not text:
            continue

        if text.lower() in ["stop", "exit", "quit"]:
            speak("Shutting down. Goodbye.")
            break

        # Quick command shortcuts
        if text.startswith("open "):
            handle_open_website(text[5:])
            continue
        if text.startswith("run "):
            handle_run_command(text[4:])
            continue

        # Otherwise ask OpenAI
        reply = ask_openai(text)
        speak(reply)

if __name__ == "__main__":
    main()
