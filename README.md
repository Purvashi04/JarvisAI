# J.A.R.V.I.S – Voice AI Assistant  

J.A.R.V.I.S (**Just A Rather Very Intelligent System**) is a Python-based voice assistant inspired by Iron Man.  
It listens to your **voice commands**, understands them with **VOSK (offline speech recognition)**, talks back using **pyttsx3**, and can connect to **OpenAI GPT models** for intelligent responses.  

---

## Features
- **Speech-to-Text (STT)** → Uses [VOSK](https://alphacephei.com/vosk/) for offline voice recognition.  
- **Text-to-Speech (TTS)** → Uses `pyttsx3` so J.A.R.V.I.S talks back.  
- **AI Responses** → Integrates with **OpenAI GPT** (requires API key).  
- **Lightweight** → Works on your PC with Python, no heavy cloud setup needed.  

---

## Project Structure
**jarvis-project**<br>
┣ jarvis_vosk.py # Main Python file<br>
┣ .env # Stores your OpenAI API key (not uploaded to GitHub)<br>
┣ vosk-model # VOSK speech recognition model folder<br>
┣ requirements.txt # Python dependencies<br>
┗ README.md # Documentation<br>
