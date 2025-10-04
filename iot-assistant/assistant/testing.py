from assistant.parser import build_parser
from assistant.sst import transcribe_from_audio
from assistant.sst import listen
import wave
import struct
import pvporcupine
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
PPN_PATH = "models/Hey-Assistant.ppn"
AUDIO_PATH = "audios_test/asss_openLight.wav"

def test_transcribe():
    for text in transcribe_from_audio("audios_test/close_lights.wav", reduce_noise=True):
        print("[RESULT]", text, "with noise reduction")

    for text in transcribe_from_audio("audios_test/close_lights.wav", reduce_noise=False):
        print("[RESULT]", text, "without noise reduction")

    for text in transcribe_from_audio("audios_test/open_door.wav", reduce_noise=True):
        print("[RESULT]", text, "with noise reduction")

    for text in transcribe_from_audio("audios_test/open_door.wav", reduce_noise=False):
        print("[RESULT]", text, "without noise reduction")

def detect_wake_word_from_wav():
    print("[WAKE] Listening to WAV file...")
    
    wf = wave.open(AUDIO_PATH, 'rb')
    if wf.getframerate() != 16000 or wf.getsampwidth() != 2 or wf.getnchannels() != 1:
        raise ValueError("Audio must be WAV format: mono, 16-bit, 16kHz.")
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[PPN_PATH],
        sensitivities=[0.7]
    )

    pcm = wf.readframes(wf.getnframes())
    pcm_unpacked = struct.unpack(f"{len(pcm) // 2}h", pcm)
    for i in range(0, len(pcm_unpacked) - porcupine.frame_length, porcupine.frame_length):
        frame = pcm_unpacked[i:i + porcupine.frame_length]
        result = porcupine.process(frame)
        if result >= 0:
            print("[WAKE] Wake word detected!")
            break
    porcupine.delete()

if __name__ == "__main__":
    # test_transcribe()
    listen()
    # detect_wake_word_from_wav()

    
