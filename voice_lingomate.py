import wave

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from ollama import chat
from piper import PiperVoice


SAMPLE_RATE = 16000
RECORD_SECONDS = 5

# Language we are currently speaking.
# English = "en"
TARGET_LANGUAGE = "en"

VOICE_MODEL = "en_US-lessac-medium.onnx"
VOICE_OUTPUT_FILE = "lingomate_reply.wav"

print("Loading speech recognition model...")
speech_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)
print("Speech model loaded!")

print("Loading voice...")
voice = PiperVoice.load(VOICE_MODEL)
print("Voice model loaded!")

def listen():
    """Record the microphone and convert the speech into text."""

    print("\nSpeak now...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )

    sd.wait()

    print("Transcribing...")

    segments, info = speech_model.transcribe(
        audio.flatten(),
        language=TARGET_LANGUAGE,
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=False,
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()

def get_response(user_text, conversation):
    """Send the user's text to LingoMate and return its response."""

    conversation.append(
        {
            "role": "user",
            "content": user_text,
        }
    )

    response = chat(
        model="qwen3:4b-instruct",
        messages=[
            {
                "role": "system",
                "content": """
You are LingoMate, a natural native-speaking conversation partner.

Understand the learner's meaning even when their language is broken.

During normal conversation:
- Do not correct grammar unless the learner asks.
- Respond naturally to what they mean.
- Keep the conversation flowing.
- Speak clearly and fairly briefly.
- Do not turn every reply into a lesson.
- Do not constantly praise the learner or ask "What's next?"
- If the learner asks for correction, then explain briefly.

The learner should feel like they are talking to a real person,
not using a language-learning exercise.
""",
            },
            *conversation,
        ],
        stream=False,
        think=False,
        options={
            "temperature": 0.7,
        },
    )

    assistant_text = response["message"]["content"].strip()

    conversation.append(
        {
            "role": "assistant",
            "content": assistant_text,
        }
    )

    return assistant_text

def speak(text):
    """Convert text to speech and play it."""

    print("\nGenerating voice...")

    with wave.open(VOICE_OUTPUT_FILE, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    with wave.open(VOICE_OUTPUT_FILE, "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        audio_bytes = wav_file.readframes(wav_file.getnframes())

    if sample_width != 2:
        raise ValueError(
            f"Expected 16-bit audio, got {sample_width * 8}-bit"
        )

    audio = np.frombuffer(audio_bytes, dtype=np.int16)

    if channels > 1:
        audio = audio.reshape(-1, channels)

    print("Speaking...")

    sd.play(audio, sample_rate)
    sd.wait()

def main():
    conversation = []

    while True:
        input("\nPress Enter to speak...")

        user_text = listen()

        if not user_text:
            print("I didn't catch that.")
            continue

        print(f"You: {user_text}")

        response = get_response(
            user_text,
            conversation,
        )

        print(f"LingoMate: {response}")
        speak(response)


if __name__ == "__main__":
    main()