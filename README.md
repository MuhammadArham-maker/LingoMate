# LingoMate

**A local-first AI conversation partner for language practice.**

LingoMate is an experimental Python project built around a simple idea: language practice should feel like communicating with someone, not constantly completing a grammar exercise. Its intended behavior is to understand what the learner is trying to say, respond naturally, and offer explicit correction or explanation when requested.

The project currently contains two related prototypes:

- **Text conversation:** a command-line conversation program using a local Ollama model, with session-level conversation memory.
- **Voice conversation:** an experimental listen–respond–speak loop connecting speech recognition, the language model, and speech synthesis.

The prototypes share the same product direction, but their memory implementations are not yet unified.

## Project Background & Early Development

LingoMate originated from the idea of building a natural
AI conversation partner rather than another conventional
language-learning application.

These early recordings document the original vision,
design philosophy and first integrated voice prototype.

- **Original Vision (September 17, 2026):**
  [Natural conversation, imperfect language and the initial
  development phases](https://youtu.be/7MssvTYP3V0?t=254)

- **First Voice Prototype (September 20, 2026):**
  [Local voice pipeline, component integration and early
  speech-recognition challenges](https://youtu.be/252Yp-8Y2HA?t=169)

## Current capabilities

### Text conversation — `Lingomate.py`

- Sends conversation messages to a local Ollama model (`qwen3:4b-instruct`).
- Uses a system prompt designed to prioritize natural conversation over unsolicited correction.
- Streams the model's response to the terminal.
- Keeps recent messages and summarizes older conversation when the session grows.
- Provides `/memory`, `/reset`, and `/quit` commands.
- Keeps session memory in program memory; it is not a persistent user database.

### Voice prototype — `voice_lingomate.py`

- Records a fixed five-second audio segment from the microphone.
- Transcribes speech using `faster-whisper` with the `small` model on CPU (`int8`).
- Sends the transcription and conversation messages to the local Ollama model.
- Generates spoken output using Piper and plays it through the computer's audio output.
- Loads the Whisper and Piper models when the program starts.

### Supporting experiments

- `speech_test.py` is an earlier standalone speech-to-text test using the Whisper `base` model.
- `tts_test.py` is a standalone Piper text-to-speech test.

## Architecture

```text
Text prototype

User text
    |
    v
Python conversation loop
    |
    v
Ollama (Qwen3)
    |
    v
Streamed text response

Session summary memory is maintained by the Python application.


Voice prototype

Microphone
    |
    v
SoundDevice
    |
    v
faster-whisper
    |
    v
Transcribed text
    |
    v
Ollama (Qwen3)
    |
    v
Response text
    |
    v
Piper
    |
    v
Speakers
```

The components are kept conceptually separate so speech recognition, conversation, and speech synthesis can be tested independently. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for implementation details and current boundaries.

## Technology

- Python
- Ollama Python client and local Ollama runtime
- Qwen3 4B Instruct (`qwen3:4b-instruct`)
- faster-whisper
- Piper TTS
- SoundDevice
- NumPy

## Development environment

The supplied project environment recorded Python 3.14.7 and the direct dependency versions pinned in [`requirements.txt`](requirements.txt). Audio-device availability and model-runtime compatibility depend on the local machine.

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Install and prepare Ollama

Install the Ollama application separately, make sure its local service is running, and download the model used by the code:

```bash
ollama pull qwen3:4b-instruct
```

The Python programs expect the local Ollama service to be available.

### 3. Prepare the Piper voice model

The repository includes the Piper voice configuration file `en_US-lessac-medium.onnx.json`, but intentionally does not include the model weights. Obtain the matching `en_US-lessac-medium.onnx` file from the official Piper voice-model distribution and place it in the project root beside the JSON configuration file.

The voice prototype currently uses this English (US) voice. The `.onnx` model weights are excluded from Git because model binaries are large assets.

### 4. Run a prototype

Text conversation:

```bash
python Lingomate.py
```

Integrated voice prototype:

```bash
python voice_lingomate.py
```

Standalone speech recognition test:

```bash
python speech_test.py
```

Standalone text-to-speech test:

```bash
python tts_test.py
```

The speech-recognition model used by faster-whisper is downloaded when first loaded if it is not already available locally.

## Current limitations

- The voice prototype records fixed five-second segments rather than using continuous, endpoint-detected conversation.
- `TARGET_LANGUAGE` is currently set to English (`en`). Multilingual support is part of the intended direction, but this voice configuration is not yet language-agnostic.
- The bundled Piper configuration is for an English (US) voice; other languages require compatible voice models.
- The voice prototype keeps an in-memory conversation list but does not use the text prototype's summary-memory system.
- Speech recognition quality is the main known weakness noted during development.
- The first interaction can be slower while local models initialize or warm up.
- The project is a working prototype, not a finished desktop or mobile application.

## Development history

The Git history contains seven development checkpoints documenting the progression of LingoMate:

1. Initial text-based conversation prototype.
2. Sliding conversation window.
3. Session summary memory.
4. Speech-to-text prototype.
5. Speech input and text-to-speech prototypes.
6. Improved speech recognition using Whisper small.
7. Piper voice integration and project documentation.

The latest checkpoint, committed on 25 November 2026, adds the Piper voice integration and supporting project documentation.

A summarized development timeline is available in [`docs/DEVELOPMENT_LOG.md`](docs/DEVELOPMENT_LOG.md).

## Repository layout

```text
LingoMate/
├── .gitignore
├── Lingomate.py
├── voice_lingomate.py
├── speech_test.py
├── tts_test.py
├── en_US-lessac-medium.onnx.json
├── requirements.txt
├── README.md
└── docs/
    ├── ARCHITECTURE.md
    └── DEVELOPMENT_LOG.md
```

## Project status

LingoMate is under active development. This repository documents the current prototypes and their actual boundaries; planned capabilities are not described as completed features.