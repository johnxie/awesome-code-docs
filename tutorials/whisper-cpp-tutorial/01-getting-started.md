---
layout: default
title: "Chapter 1: Getting Started with Whisper.cpp"
parent: "Whisper.cpp Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Whisper.cpp

Welcome to Whisper.cpp! If you've ever wanted to add speech recognition capabilities to your applications, you're in the right place. Whisper.cpp brings the power of OpenAI's Whisper model to C/C++ applications with exceptional performance and minimal dependencies.

## What Problem Does Whisper.cpp Solve?

Traditional speech recognition solutions often require:
- **Expensive cloud APIs** with usage costs and latency
- **GPU requirements** for acceptable performance
- **Internet connectivity** for processing
- **Complex setup** with multiple dependencies

Whisper.cpp solves these problems by:
- **Running entirely offline** - no internet required
- **Using only CPU** - works on any computer without GPU
- **Minimal dependencies** - just a C++ compiler
- **Cross-platform** - runs on Windows, macOS, Linux, and embedded devices

## Installing Whisper.cpp

Let's get started with the installation process. Whisper.cpp is designed to be easy to build and use.

### Step 1: Clone the Repository

```bash
# Clone the Whisper.cpp repository
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp

# Check the contents
ls -la
```

### Step 2: Build the Project

Whisper.cpp uses a simple Makefile build system:

```bash
# Build the main executable and library
make

# For faster builds on multi-core systems
make -j$(nproc)

# Build with debug symbols (useful for development)
make debug
```

### Step 3: Download a Model

Whisper.cpp needs a pre-trained model to work:

```bash
# Download the base English model (74MB)
./models/download-ggml-model.sh base.en

# Or download the base multilingual model (74MB)
./models/download-ggml-model.sh base

# For better accuracy, download medium model (500MB)
./models/download-ggml-model.sh medium.en
```

## How It Works Under the Hood

Before we run our first transcription, let's understand what just happened:

### The Build Process
When you run `make`, Whisper.cpp:
1. **Compiles the C++ source** into object files
2. **Links against system libraries** (no external dependencies needed)
3. **Creates the main executable** (`main`) and shared library (`libwhisper.so`)

### Model Files
The downloaded model files contain:
- **Neural network weights** - trained parameters for speech recognition
- **GGML format** - optimized binary format for fast loading
- **Quantized weights** - reduced precision for better performance

## Your First Transcription

Let's transcribe some audio! First, you'll need an audio file. Whisper.cpp supports WAV, MP3, M4A, and many other formats.

### Step 1: Prepare Audio

```bash
# If you don't have audio, you can use the built-in test
# Or record something: (on macOS/Linux)
rec test.wav trim 0 10  # Record 10 seconds

# Or download a sample (if you have curl)
curl -L https://upload.wikimedia.org/wikipedia/commons/1/1f/Apollo_11_first_step.ogg -o sample.ogg
```

### Step 2: Run Transcription

```bash
# Basic transcription
./main -f test.wav

# With specific model
./main -m models/ggml-base.en.bin -f test.wav

# With timestamps
./main -f test.wav --print-timestamps

# Verbose output
./main -f test.wav -v
```

### Step 3: Understand the Output

```
whisper_init_from_file_with_params_no_state: loading model from 'models/ggml-base.en.bin'
whisper_model_load: loading model
whisper_model_load: n_vocab       = 51865
whisper_model_load: n_audio_ctx   = 1500
whisper_model_load: n_audio_state = 512
whisper_model_load: n_audio_head  = 8
whisper_model_load: n_text_ctx    = 448
whisper_model_load: n_text_state  = 512
whisper_model_load: n_text_head   = 8

[00:00:00.000 --> 00:00:03.000]  Hello, this is a test of Whisper.cpp
```

## Core Components Explained

### 1. The Main Executable
The `main` program you just built provides:
- **Command-line interface** for easy testing
- **All core functionality** wrapped in a simple interface
- **Example usage** for your own applications

### 2. Model Architecture
Whisper models consist of:
- **Audio Encoder**: Converts audio to representations
- **Text Decoder**: Generates text from audio features
- **Cross-attention**: Connects audio and text processing

### 3. GGML Backend
GGML (Georgi Gerganov Machine Learning) provides:
- **Tensor operations** optimized for CPU
- **Memory efficiency** through quantization
- **Cross-platform support** with SIMD optimizations

## Basic Usage Patterns

### Command Line Options

```bash
# Show all options
./main --help

# Common usage patterns:
./main -m models/ggml-base.en.bin -f audio.wav                    # Basic transcription
./main -f audio.wav --language en                                 # Force English
./main -f audio.wav --print-colors                               # Color output
./main -f audio.wav --max-len 50                                 # Limit output length
./main -f audio.wav --speed-up                                   # Faster processing
./main -f audio.wav -otxt                                       # Output to text file
```

### Understanding Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-m` | Model file path | `-m models/ggml-base.en.bin` |
| `-f` | Audio file path | `-f recording.wav` |
| `--language` | Force language | `--language es` |
| `--print-timestamps` | Show timing info | `--print-timestamps` |
| `--max-len` | Max output length | `--max-len 100` |

## Building Your First Application

Now let's create a simple C++ program that uses Whisper.cpp:

```cpp
// simple_transcriber.cpp
#include "whisper.h"
#include <iostream>
#include <string>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " <model_path> <audio_path>" << std::endl;
        return 1;
    }

    // Initialize Whisper context
    struct whisper_context *ctx = whisper_init_from_file(argv[1]);
    if (ctx == nullptr) {
        std::cout << "Failed to load model" << std::endl;
        return 1;
    }

    // Process audio file
    if (whisper_pcm_to_mel(ctx, argv[2], 0, whisper_n_samples(ctx)) != 0) {
        std::cout << "Failed to process audio" << std::endl;
        return 1;
    }

    // Run inference
    whisper_full_params params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    params.print_progress = false;
    params.print_special = false;
    params.print_realtime = false;

    if (whisper_full(ctx, params, nullptr, 0) != 0) {
        std::cout << "Failed to run inference" << std::endl;
        return 1;
    }

    // Print results
    const int n_segments = whisper_full_n_segments(ctx);
    for (int i = 0; i < n_segments; ++i) {
        const char *text = whisper_full_get_segment_text(ctx, i);
        const int64_t t0 = whisper_full_get_segment_t0(ctx, i);
        const int64_t t1 = whisper_full_get_segment_t1(ctx, i);

        printf("[%s --> %s] %s\n",
               to_timestamp(t0).c_str(),
               to_timestamp(t1).c_str(),
               text);
    }

    // Cleanup
    whisper_free(ctx);
    return 0;
}
```

### Building the Application

```bash
# Compile with Whisper.cpp
g++ -I. simple_transcriber.cpp libwhisper.a -o simple_transcriber

# Run it
./simple_transcriber models/ggml-base.en.bin audio.wav
```

## Troubleshooting Common Issues

### Model Loading Errors

```bash
# Error: "whisper_init_from_file: failed to load model"
# Solution: Check model file path and permissions
ls -la models/ggml-base.en.bin
file models/ggml-base.en.bin

# Try downloading again
./models/download-ggml-model.sh base.en
```

### Audio Format Issues

```bash
# Error: "whisper_pcm_to_mel: failed to load audio"
# Solution: Check audio file format and convert if needed

# Convert to WAV using ffmpeg
ffmpeg -i audio.mp3 -acodec pcm_s16le -ar 16000 audio.wav

# Check audio properties
ffprobe audio.wav
```

### Memory Issues

```bash
# Error: "out of memory"
# Solution: Use smaller model or add swap space

# Check available memory
free -h

# Use smaller model
./models/download-ggml-model.sh tiny.en  # Only 39MB
```

## Performance Expectations

| Model Size | Memory Usage | Speed | Accuracy |
|------------|--------------|-------|----------|
| tiny | ~200MB | ~10x realtime | Good |
| base | ~300MB | ~8x realtime | Better |
| small | ~1GB | ~4x realtime | Very good |
| medium | ~2GB | ~2x realtime | Excellent |

*Speeds measured on modern CPU. GPU acceleration can improve performance significantly.*

## What We've Accomplished

Excellent! 🎉 You've successfully:

1. **Installed Whisper.cpp** from source code
2. **Downloaded and used** pre-trained models
3. **Transcribed your first audio** file
4. **Understood the core architecture** and components
5. **Created a basic C++ application** using the library
6. **Learned troubleshooting** techniques for common issues

## Next Steps

Now that you have Whisper.cpp working, let's dive deeper into audio processing concepts. In [Chapter 2: Audio Processing Fundamentals](02-audio-processing.md), we'll explore how audio files are processed and prepared for speech recognition.

---

**Practice what you've learned:**
1. Try transcribing audio in different languages
2. Experiment with different model sizes and compare results
3. Record your own audio and test the transcription accuracy
4. Modify the simple transcriber to add custom formatting

*What kind of speech recognition application are you most excited to build?* 🎤

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `audio`, `main` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Whisper.cpp` as an operating subsystem inside **Whisper.cpp Tutorial: High-Performance Speech Recognition in C/C++**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `base`, `models`, `ggml` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Whisper.cpp` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `audio` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `main`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ggml-org/whisper.cpp)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `model` and `audio` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Audio Processing Fundamentals](02-audio-processing.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
