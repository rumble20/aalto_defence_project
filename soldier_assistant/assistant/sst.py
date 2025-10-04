import os
import noisereduce as nr
import numpy as np
import queue
import sounddevice as sd
import vosk
import json
import wave
from assistant.parser import parser_text
from assistant.parser import build_parser
import re

model_path = "models/vosk-model-small-en-us-0.15"

if not os.path.exists(model_path):
    raise FileNotFoundError("Vosk model not found in models/. Run setup.sh first.")

model = vosk.Model(model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(f"[AUDIO WARNING] {status}")
    audio = np.frombuffer(indata, dtype=np.int16)
    reduced = nr.reduce_noise(y=audio, sr=16000)
    q.put(reduced.astype(np.int16).tobytes())

def listen_and_transcribe():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("[STT] Listening...")
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print(f"[STT] You said: {text}")
                    yield text

def transcribe_from_audio(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    with wave.open(file_path, "rb") as wf:
        if wf.getframerate() != 16000 or wf.getnchannels() != 1:
            raise ValueError("Audio must be mono and 16kHz.")
        
        audio_data = wf.readframes(wf.getnframes())
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        audio_bytes = audio_np.astype(np.int16).tobytes()

        rec = vosk.KaldiRecognizer(model, 16000)
        rec.AcceptWaveform(audio_bytes)
        result = json.loads(rec.FinalResult())
        text = result.get("text", "")
        if text:
            yield text

def clean_command(text: str) -> str:
    text = text.lower()
    replacements = [
        # Misrecognized phrases
        (r"\btwo off\b", "turn off"),
        (r"\btwo on\b", "turn on"),
        (r"\bto off\b", "turn off"),
        (r"\bto on\b", "turn on"),
        (r"\btoward off\b", "turn off"),
        (r"\btoward on\b", "turn on"),
        (r"\bso off\b", "turn off"),
        (r"\bso on\b", "turn on"),
        (r"\bjordan off\b", "turn off"),
        (r"\bjordan on\b", "turn on"),
        (r"\btorrent of\b", "turn off"),
        (r"\btorrent on\b", "turn on"),

        (r"\bblows\b", "close"),
    
        # Misheard devices
        (r"\blite\b", "light"),
        
        # Fix common speech slurring
        (r"\bturnon\b", "turn on"),
        (r"\bturnoff\b", "turn off"),
        (r"\bturnitoff\b", "turn off"),
        (r"\bturniton\b", "turn on"),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text

def listen():
    parser = build_parser()
    for text in listen_and_transcribe():
        print(f"[MAIN] Received: {text}")
        cleaned = clean_command(text)
        print(f"[CLEANED] {cleaned}")
        temp = parser_text(parser, text)
        print(f"[TMP] {temp}")

def listen_once():
    print("[STT] Listening for a command...")
    rec = vosk.KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text
