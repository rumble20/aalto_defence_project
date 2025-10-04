import struct
import pvporcupine
import pyaudio
import os
import json
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv

from assistant.sst import model as vosk_model
from assistant.sst import clean_command
from assistant.parser import build_parser, parser_text

# Load env vars
load_dotenv()
ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
PPN_PATH = "models/Hey-Assistant.ppn"

# ========== Setup ==========
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[PPN_PATH],
    sensitivities=[0.7]
)

parser = build_parser()
recognizer = KaldiRecognizer(vosk_model, 16000)

pa = pyaudio.PyAudio()
stream = pa.open(
    rate=16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

def listen_for_command():
    print("[ASSISTANT] Listening for a command...")
    recognizer.Reset()
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            return text

def handle_command(raw_text):
    print(f"[COMMAND] Raw: {raw_text}")
    cleaned = clean_command(raw_text)
    print(f"[COMMAND] Cleaned: {cleaned}")
    intent = parser_text(parser, cleaned)
    print(f"[INTENT] {intent}")

def main_loop():
    print("[WAKE] Waiting for wake word...")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm_unpacked)
            if result >= 0:
                print("[WAKE] Wake word detected!")
                command = listen_for_command()
                if command:
                    handle_command(command)
                print("[WAKE] Listening again...")
    except KeyboardInterrupt:
        print("[SYSTEM] Interrupted by user.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main_loop()
