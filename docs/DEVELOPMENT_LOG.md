# LingoMate Development Log

This is a concise account of the development stages recorded in the project's original notes and Git history. It is a summary, not a replacement for the original working notebook.

## Project idea and behavior

The initial concept was an AI conversation partner for language practice. The product direction emphasized conversation over lessons: understand imperfect attempts, respond to intended meaning, avoid correcting every mistake, and explain language when the learner explicitly asks. Multilingual and spontaneous beginner input were part of the intended direction.

## Text conversation prototype

The first implementation connected a Python command-line program to a locally running Ollama model (`qwen3:4b-instruct`). Early tests with the raw model showed that it tended to behave like a language tutor: correcting grammar, offering alternative phrases, and pushing lessons. Those tests informed the system prompt and the interaction rules in `Lingomate.py`.

The text prototype then gained session memory. It began with a sliding window of recent messages and later added summary-based compression of older messages. The current program retains recent messages and uses a model-generated summary to carry forward selected context during the same running session. The notes also record that summary quality needed improvement and that the decision was to keep memory modest for the first version.

## Local model performance

The notes document troubleshooting Ollama's GPU initialization on the development laptop. The model was first made to run on CPU, and later the environment was adjusted so Ollama detected the NVIDIA RTX 2050 and split model execution across available resources. The development notes report a noticeable response-time improvement after GPU use was restored.

## Speech recognition experiments

Speech input was developed as a separate experiment before being attached to the conversation loop. `speech_test.py` uses `sounddevice` to record microphone audio and faster-whisper to transcribe it. Early tests revealed recognition errors, especially with short speech and language/script handling. The integrated voice script was later moved from the Whisper `base` model to `small`, with CPU `int8` inference, an explicit English target language, VAD filtering, and previous-text conditioning disabled.

## Text-to-speech experiments

Piper was tested separately in `tts_test.py`. The test program loads the `en_US-lessac-medium` voice, synthesizes a WAV file, and plays it through `sounddevice`. The voice configuration JSON is included in the project; the ONNX model weights are kept outside Git.

## Voice integration

The experimental `voice_lingomate.py` connects the microphone, faster-whisper, Ollama, and Piper. The current snapshot records a five-second audio segment, transcribes it, sends the recognized text to Qwen3, generates a response, synthesizes speech, and plays it. The notes describe this as the first complete voice architecture, while identifying transcription accuracy and first-response latency as remaining limitations.

## Git checkpoints preserved

The repository's Git history contains seven development checkpoints documenting the progression of LingoMate:

1. Initial LingoMate conversation prototype — 18 September 2026.
2. Add sliding conversation window — 19 September 2026.
3. Add session summary memory — 19 September 2026.
4. Add speech-to-text prototype — 19 September 2026.
5. Add speech input and text-to-speech prototypes — 19 September 2026.
6. Improve speech recognition with Whisper small — 20 September 2026.
7. Add Piper voice integration and project documentation — 25 November 2026.

Together, these commits document the development of LingoMate from its initial text-based conversation prototype through session memory, speech recognition, text-to-speech experiments and the integration of a complete voice interaction pipeline.
