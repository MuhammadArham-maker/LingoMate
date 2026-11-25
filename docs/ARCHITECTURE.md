# LingoMate Architecture

## 1. Product direction

LingoMate is intended to act as a natural conversation partner first, with language-teaching behavior available when the learner asks for it. The design priorities recorded during development are: understand the learner's intention, respond naturally, maintain conversational flow, model useful language through replies, and provide explicit correction only on request.

This is the intended interaction model. The current prompt attempts to encode it; it should not be read as a guarantee that every model response will follow it perfectly.

## 2. Text conversation prototype

`Lingomate.py` contains the text-based conversation loop.

1. The program stores the current conversation as a list of user and assistant messages.
2. `build_context_messages()` combines the system instructions, optional session summary, and retained conversation messages.
3. The Ollama Python client sends the context to `qwen3:4b-instruct`.
4. The program streams the response to the terminal and adds it to the conversation.
5. When the message count exceeds the configured summary threshold, `summarize_old_messages()` asks the same local model to compress older messages. The newest messages are retained and the summary is added to the system context.

The current constants retain up to 12 recent messages and trigger summarization after the conversation exceeds 16 messages. `/memory` displays the session summary and recent-message count; `/reset` clears the current session; `/quit` exits.

Session memory exists only while the program is running. There is no permanent user database or cross-session profile store in this implementation.

## 3. Voice conversation prototype

`voice_lingomate.py` implements a separate experimental voice loop.

```text
Microphone
   -> sounddevice records 5 seconds at 16 kHz
   -> faster-whisper small model (CPU, int8; English forced)
   -> recognized text
   -> Ollama / qwen3:4b-instruct
   -> response text
   -> Piper voice synthesis
   -> WAV audio playback through sounddevice
```

The Whisper and Piper models are loaded when the script starts. Piper writes synthesized speech to `lingomate_reply.wav`, which is then read and played.

The voice script maintains a simple in-memory message list for the current run. It does not currently call the summarization functions from `Lingomate.py`, and the two entry points are separate programs rather than one unified application.

## 4. Supporting experiments

- `speech_test.py` tests microphone capture and faster-whisper transcription independently. It currently uses the `base` Whisper model and automatic language detection.
- `tts_test.py` tests Piper voice synthesis and audio playback independently.

These files document the component-first development approach: test the microphone/transcriber and voice synthesizer separately, then connect them in the voice prototype.

## 5. Models and local runtime

- **LLM runtime:** Ollama, running locally.
- **Conversation model:** `qwen3:4b-instruct`.
- **Speech recognition:** faster-whisper `small` in the integrated voice script; `base` in the standalone test.
- **Speech synthesis:** Piper with the `en_US-lessac-medium` voice.

Model weights are not stored in this repository. The Piper JSON configuration is included; its matching ONNX weights must be obtained separately. Ollama and faster-whisper manage their own model downloads/caches.

## 6. Known boundaries

- The voice prototype records fixed-duration chunks; it does not yet detect natural end-of-speech or support barge-in/interruptions.
- The voice transcription language is currently hard-coded to English.
- The current Piper voice is English (US).
- The text conversation prototype has summary-based session memory; the voice prototype does not share that memory implementation.
- Speech recognition quality and initial model-loading latency were identified in the development notes as the main areas needing further work.
