import struct
import pvporcupine
import pyaudio
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
PPN_PATH = "models/Hey-Assistant.ppn"

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[PPN_PATH],
    sensitivities=[0.7]
)

pa = pyaudio.PyAudio()
stream = pa.open(
    rate=16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

def wait_for_wake_word():
    print("[WAKE] Waiting for wake word...")
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm_unpacked)
        if result >= 0:
            print("[WAKE] Wake word detected!")
            return

def cleanup():
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
