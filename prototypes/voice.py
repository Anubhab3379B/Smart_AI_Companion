# File: voice.py
"""
Voice module for your AI assistant.
- Updated to fix ModuleNotFoundError: replaces 'whisper' with 'openai-whisper' CLI fallback.
- Still supports ElevenLabs TTS with pyttsx3 fallback.
- Each line documented.
"""

import os
import subprocess
import requests
import pyttsx3 # type: ignore
import sounddevice as sd # type: ignore
import numpy as np
import scipy.io.wavfile

# Speech to text: use Whisper CLI fallback
# You must install OpenAI's whisper with `pip install openai-whisper` and `ffmpeg`

def record_audio(filename="temp.wav", duration=5, fs=44100):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()
    scipy.io.wavfile.write(filename, fs, audio)
    return filename

# Transcribe using whisper CLI
# safer in sandboxed or limited environments

def transcribe_audio(filename):
    print("Transcribing with whisper CLI...")
    result = subprocess.run(["whisper", filename, "--model", "base", "--language", "en", "--output_format", "txt"], capture_output=True, text=True)
    transcript_file = filename.replace(".wav", ".txt")
    if os.path.exists(transcript_file):
        with open(transcript_file) as f:
            return f.read().strip()
    return "(could not transcribe)"

# ElevenLabs TTS (fallback to pyttsx3)
EL_API_KEY = os.getenv("ELEVEN_API_KEY")

def speak(text):
    if EL_API_KEY:
        response = requests.post(
            "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>",
            headers={"xi-api-key": EL_API_KEY, "Content-Type": "application/json"},
            json={"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}
        )
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        os.system("mpg123 output.mp3")
    else:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# Example usage
if __name__ == "__main__":
    file = record_audio()
    text = transcribe_audio(file)
    print(f"You said: {text}")
    speak("I heard you say " + text)