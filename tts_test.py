import os
import wave

import numpy as np
import sounddevice as sd
from piper import PiperVoice


VOICE_MODEL = "en_US-lessac-medium.onnx"
OUTPUT_FILE = "tts_test.wav"


print("Loading voice...")

voice = PiperVoice.load(VOICE_MODEL)

print("Voice loaded!")

text = input("What should I say? ")

print("Generating speech...")

with wave.open(OUTPUT_FILE, "wb") as wav_file:
    voice.synthesize_wav(text, wav_file)

print("Speech generated.")

with wave.open(OUTPUT_FILE, "rb") as wav_file:
    sample_rate = wav_file.getframerate()
    channels = wav_file.getnchannels()
    sample_width = wav_file.getsampwidth()
    audio_bytes = wav_file.readframes(wav_file.getnframes())

if sample_width != 2:
    raise ValueError(f"Expected 16-bit audio, got {sample_width * 8}-bit")

audio = np.frombuffer(audio_bytes, dtype=np.int16)

if channels > 1:
    audio = audio.reshape(-1, channels)

print("Speaking...")

sd.play(audio, sample_rate)
sd.wait()

print("Finished.")