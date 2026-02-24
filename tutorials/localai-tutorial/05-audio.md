---
layout: default
title: "LocalAI Tutorial - Chapter 5: Audio Processing"
nav_order: 5
has_children: false
parent: LocalAI Tutorial
---

# Chapter 5: Audio Processing - Whisper & TTS

Welcome to **Chapter 5: Audio Processing - Whisper & TTS**. In this part of **LocalAI Tutorial: Self-Hosted OpenAI Alternative**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Transcribe speech to text with Whisper and generate speech with text-to-speech models.

## Overview

LocalAI supports audio processing through Whisper (speech-to-text) and various TTS (text-to-speech) models, all running locally.

## Installing Audio Models

### Whisper Models

```bash
# Install base Whisper model
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "whisper-base"}'

# Install larger models for better accuracy
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "whisper-large-v3"}'
```

### TTS Models

```bash
# Install Piper TTS
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "tts-1"}'

# Install Coqui TTS
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "coqui-tts"}'
```

## Speech-to-Text with Whisper

### Basic Transcription

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

# Transcribe audio file
with open("audio.wav", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print("Transcription:", transcription.text)
```

### Direct API Call

```bash
# Transcribe via API
curl -X POST http://localhost:8080/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav" \
  -F "model=whisper-1"
```

## Advanced Whisper Features

### Language Specification

```python
# Specify language for better accuracy
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="en",  # ISO language code
    temperature=0.0  # Deterministic results
)
```

### Translation

```python
# Translate to English
translation = client.audio.translations.create(
    model="whisper-1",
    file=foreign_audio_file
)

print("English translation:", translation.text)
```

### Timestamped Output

```python
# Get word-level timestamps
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word"]
)

for segment in transcription.segments:
    print(f"{segment.start:.2f}s - {segment.end:.2f}s: {segment.text}")
```

## Text-to-Speech

### Basic TTS

```python
# Generate speech
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
    input="Hello, this is LocalAI speaking!",
    response_format="mp3"
)

# Save audio
with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

### Voice Options

```python
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

for voice in voices:
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=f"This is the {voice} voice.",
        response_format="mp3"
    )

    with open(f"voice_{voice}.mp3", "wb") as f:
        f.write(response.content)
```

## Audio Processing Pipeline

### Transcribe and Respond

```python
def audio_conversation(audio_file_path):
    """Transcribe audio, generate response, and create speech reply."""

    # Step 1: Transcribe
    with open(audio_file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    user_text = transcription.text
    print(f"User said: {user_text}")

    # Step 2: Generate AI response
    chat_response = client.chat.completions.create(
        model="phi-2",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Keep responses concise."},
            {"role": "user", "content": user_text}
        ],
        max_tokens=100
    )

    ai_text = chat_response.choices[0].message.content
    print(f"AI response: {ai_text}")

    # Step 3: Convert to speech
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=ai_text,
        response_format="mp3"
    )

    # Save reply
    output_file = "ai_reply.mp3"
    with open(output_file, "wb") as f:
        f.write(speech_response.content)

    return output_file

# Usage
reply_audio = audio_conversation("user_question.wav")
print(f"AI reply saved to: {reply_audio}")
```

## Batch Audio Processing

### Multiple Files

```python
import os
from concurrent.futures import ThreadPoolExecutor

def transcribe_file(file_path):
    """Transcribe a single audio file."""
    try:
        with open(file_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="json"
            )
        return {
            "file": file_path,
            "text": result.text,
            "success": True
        }
    except Exception as e:
        return {
            "file": file_path,
            "error": str(e),
            "success": False
        }

def batch_transcribe(audio_dir, max_workers=4):
    """Transcribe all audio files in directory."""
    audio_files = []
    for ext in ['.wav', '.mp3', '.m4a', '.flac']:
        audio_files.extend([
            os.path.join(audio_dir, f)
            for f in os.listdir(audio_dir)
            if f.endswith(ext)
        ])

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(transcribe_file, audio_files))

    return results

# Usage
results = batch_transcribe("audio_files/")

successful = [r for r in results if r["success"]]
failed = [r for r in results if not r["success"]]

print(f"Successfully transcribed: {len(successful)} files")
print(f"Failed: {len(failed)} files")

# Save results
with open("transcriptions.txt", "w") as f:
    for result in successful:
        f.write(f"File: {result['file']}\n")
        f.write(f"Text: {result['text']}\n\n")
```

## Audio Quality Optimization

### Whisper Settings

```python
# High accuracy transcription
transcription = client.audio.transcriptions.create(
    model="whisper-large-v3",  # Use largest model
    file=audio_file,
    language="en",
    temperature=0.0,  # Deterministic
    initial_prompt="This is a clear recording of a technical discussion.",  # Context
    no_speech_threshold=0.3,  # Filter out silence
    compression_ratio_threshold=2.0  # Filter out repetitive speech
)
```

### TTS Quality

```python
# High quality speech synthesis
speech = client.audio.speech.create(
    model="tts-1-hd",  # HD quality if available
    voice="alloy",
    input=text,
    response_format="mp3",
    speed=1.0  # Speech rate (0.25-4.0)
)
```

## Custom Audio Models

### Installing Custom Whisper

```yaml
# Custom Whisper configuration
name: whisper-custom
backend: whisper
parameters:
  model: whisper-models/ggml-large-v3.bin
  language: auto
  translate: false
  threads: 4
  processors: 1
  offset_ms: 0
  duration_ms: 0
```

### Custom TTS Voices

```yaml
# Custom TTS configuration
name: custom-tts
backend: piper
parameters:
  model: piper-models/en_US-lessac-medium.onnx
  speaker: 0
  length_scale: 1.0
  noise_scale: 0.667
  noise_w: 0.8
```

## Real-time Audio Processing

### Streaming Transcription (if supported)

```python
# Real-time transcription simulation
import time

def simulate_realtime_transcription(audio_chunks):
    """Process audio in chunks for near real-time transcription."""
    full_transcription = ""

    for i, chunk in enumerate(audio_chunks):
        # Save chunk to temporary file
        chunk_file = f"temp_chunk_{i}.wav"
        with open(chunk_file, "wb") as f:
            f.write(chunk)

        # Transcribe chunk
        with open(chunk_file, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        full_transcription += result.text + " "

        # Clean up
        os.remove(chunk_file)

        # Small delay to simulate real-time processing
        time.sleep(0.1)

    return full_transcription.strip()

# Usage (would need actual audio chunking logic)
# transcription = simulate_realtime_transcription(audio_chunks)
```

## Audio Format Support

### Supported Formats

- **WAV**: Uncompressed, highest quality
- **MP3**: Compressed, good quality
- **M4A/AAC**: Compressed, good quality
- **FLAC**: Lossless compression
- **OGG**: Open format with compression

### Format Conversion

```bash
# Convert audio formats using ffmpeg
ffmpeg -i input.mp3 -acodec pcm_s16le -ar 16000 output.wav

# Batch conversion
for file in *.mp3; do
    ffmpeg -i "$file" -acodec pcm_s16le -ar 16000 "${file%.mp3}.wav"
done
```

## Performance Optimization

### CPU Optimization

```yaml
# CPU-optimized Whisper
name: whisper-cpu
backend: whisper
parameters:
  model: whisper-models/ggml-base.bin  # Smaller model
  threads: 8  # Match CPU cores
  processors: 1
  language: en  # Specify language if known
```

### GPU Acceleration

```yaml
# GPU-accelerated Whisper (if supported)
name: whisper-gpu
backend: whisper
parameters:
  model: whisper-models/ggml-large-v3.bin
  gpu_layers: 50  # Offload to GPU
  main_gpu: 0
  tensor_split: 0.5,0.5  # Multi-GPU split
```

## Integration Examples

### Voice Assistant

```python
class VoiceAssistant:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:8080/v1", api_key="dummy")

    def process_audio_command(self, audio_file):
        """Process voice command and respond."""
        # Transcribe
        with open(audio_file, "rb") as f:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        command = transcription.text.lower().strip()
        print(f"Command: {command}")

        # Process command
        if "weather" in command:
            response_text = "The weather is sunny today."
        elif "time" in command:
            from datetime import datetime
            response_text = f"The current time is {datetime.now().strftime('%H:%M')}."
        else:
            # Use AI for general responses
            chat_response = self.client.chat.completions.create(
                model="phi-2",
                messages=[{"role": "user", "content": transcription.text}],
                max_tokens=50
            )
            response_text = chat_response.choices[0].message.content

        # Generate speech response
        speech = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=response_text
        )

        return speech.content, response_text

# Usage
assistant = VoiceAssistant()
audio_response, text_response = assistant.process_audio_command("command.wav")

with open("response.mp3", "wb") as f:
    f.write(audio_response)
```

## Troubleshooting

### Whisper Issues

**Poor transcription quality:**
```bash
# Use larger model
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "whisper-large-v3"}'
```

**Language detection issues:**
```bash
# Specify language explicitly
curl -X POST http://localhost:8080/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav" \
  -F "model=whisper-1" \
  -F "language=en"
```

### TTS Issues

**Poor voice quality:**
```bash
# Try different voices
curl -X POST http://localhost:8080/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "voice": "nova", "input": "Hello"}' \
  --output speech.mp3
```

**Slow synthesis:**
```bash
# Use faster TTS model
curl -X POST http://localhost:8080/models/apply \
  -H "Content-Type: application/json" \
  -d '{"id": "piper-tts"}'
```

## Best Practices

1. **Audio Quality**: Use high-quality, clear recordings for best transcription
2. **File Formats**: WAV preferred for Whisper, MP3 acceptable
3. **Language**: Specify language when known for better accuracy
4. **Context**: Provide initial prompts for domain-specific transcription
5. **Batch Processing**: Process multiple files efficiently with threading
6. **Error Handling**: Implement retry logic for network/audio issues
7. **Resource Management**: Monitor CPU/GPU usage during processing

Next: Generate vector embeddings for semantic search and RAG applications.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `audio`, `whisper` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Audio Processing - Whisper & TTS` as an operating subsystem inside **LocalAI Tutorial: Self-Hosted OpenAI Alternative**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `file`, `client`, `create` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Audio Processing - Whisper & TTS` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `audio` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `whisper`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/mudler/LocalAI)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `model` and `audio` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Image Generation with Stable Diffusion](04-image-generation.md)
- [Next Chapter: Chapter 6: Vector Embeddings for RAG](06-embeddings.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
