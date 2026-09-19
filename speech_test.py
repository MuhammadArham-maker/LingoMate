import sounddevice as sd
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
RECORD_SECONDS = 5


print("Loading speech recognition model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8",
)

print("Model loaded!")


input("Press Enter and then speak for 5 seconds...")

print("Recording...")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
)

sd.wait()

print("Recording finished.")
print("Transcribing...")

segments, info = model.transcribe(
    audio.flatten(),
    beam_size=5,
)

text = ""

for segment in segments:
    text += segment.text

print("\nYou said:")
print(text.strip())