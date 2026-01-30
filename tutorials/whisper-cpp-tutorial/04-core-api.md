---
layout: default
title: "Chapter 4: Core API & Usage Patterns"
nav_order: 4
has_children: false
parent: "Whisper.cpp Tutorial"
---

# Chapter 4: Core API & Usage Patterns

> Mastering Whisper.cpp's C/C++ API for speech recognition applications

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- Core Whisper.cpp API functions and data structures
- Common usage patterns for transcription and translation
- Error handling and resource management
- Integration with C/C++ applications
- Advanced API features and callbacks

## 🏗️ Core API Architecture

### **Main Data Structures**

```cpp
// Core context structure
struct whisper_context {
    whisper_model model;
    whisper_state * state;
    ggml_context * ctx;

    // Audio processing
    whisper_mel mel;
    float * pcmf32;  // PCM audio data
    int pcmf32_len;

    // Token processing
    whisper_token * tokens;
    int tokens_len;
    int tokens_max;

    // Language detection
    int lang_id;
    float lang_proba;

    // Threading
    int n_threads;
};

// Model loading parameters
struct whisper_context_params {
    bool use_gpu;              // Use GPU if available (GGML)
    int gpu_device;            // GPU device index
    int dtw_token_timestamps;  // DTW token timestamps
    int dtw_aheads_preset;     // DTW aheads preset
    int dtw_n_top;            // DTW n top
    size_t dtw_mem_size;       // DTW memory size
};

// Full processing parameters
struct whisper_full_params {
    // General
    int strategy;              // Sampling strategy
    int n_threads;             // Number of threads
    int n_max_text_ctx;        // Max text context
    int offset_ms;             // Start offset in ms
    int duration_ms;           // Audio duration to process

    // Language
    const char * language;     // Language code (e.g., "en", "es")
    bool detect_language;      // Auto-detect language

    // Translation
    bool translate;            // Translate to English

    // Tokens
    int initial_prompt_tokens; // Initial prompt tokens
    int prompt_tokens;         // Prompt tokens array
    int n_prompt_tokens;       // Number of prompt tokens

    // Decoding
    int temperature;           // Sampling temperature
    int max_initial_ts;        // Max initial timestamps
    int length_penalty;        // Length penalty

    // Logging
    whisper_log_callback log_callback;
    void * log_callback_user_data;

    // Progress
    whisper_progress_callback progress_callback;
    void * progress_callback_user_data;

    // New tokens
    whisper_new_segment_callback new_segment_callback;
    void * new_segment_callback_user_data;

    // Encoder begin
    whisper_encoder_begin_callback encoder_begin_callback;
    void * encoder_begin_callback_user_data;
};
```

## 🚀 Basic Usage Patterns

### **Simple Transcription**

```cpp
#include "whisper.h"

// Basic transcription example
int main(int argc, char * argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <wav file>\n", argv[0]);
        return 1;
    }

    // Initialize Whisper
    struct whisper_context_params cparams = whisper_context_default_params();
    struct whisper_context * ctx = whisper_init_from_file_with_params("models/ggml-base.bin", cparams);

    if (!ctx) {
        fprintf(stderr, "Failed to initialize Whisper context\n");
        return 1;
    }

    // Load audio file
    std::vector<float> pcmf32;
    if (!read_wav_file(argv[1], pcmf32)) {
        fprintf(stderr, "Failed to read WAV file\n");
        whisper_free(ctx);
        return 1;
    }

    // Set up parameters
    struct whisper_full_params wparams = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    wparams.print_realtime   = true;
    wparams.print_progress   = false;
    wparams.print_timestamps = true;
    wparams.print_special    = false;
    wparams.translate        = false;
    wparams.language         = "en";
    wparams.n_threads        = std::min(4, (int)std::thread::hardware_concurrency());
    wparams.offset_ms        = 0;

    // Run transcription
    if (whisper_full(ctx, wparams, pcmf32.data(), pcmf32.size()) != 0) {
        fprintf(stderr, "Failed to process audio\n");
        whisper_free(ctx);
        return 1;
    }

    // Print results
    const int n_segments = whisper_full_n_segments(ctx);
    for (int i = 0; i < n_segments; ++i) {
        const char * text = whisper_full_get_segment_text(ctx, i);
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

### **Advanced Transcription with Callbacks**

```cpp
// Transcription with progress callbacks
struct CallbackData {
    int progress;
    std::string current_segment;
};

void whisper_progress_callback(struct whisper_context * ctx, struct whisper_state * state, int progress, void * user_data) {
    CallbackData * data = (CallbackData *)user_data;
    data->progress = progress;

    fprintf(stderr, "Progress: %d%%\n", progress);
}

void whisper_new_segment_callback(struct whisper_context * ctx, struct whisper_state * state, int n_new, void * user_data) {
    CallbackData * data = (CallbackData *)user_data;

    const int n_segments = whisper_full_n_segments(ctx);
    for (int i = n_segments - n_new; i < n_segments; ++i) {
        const char * text = whisper_full_get_segment_text(ctx, i);
        const int64_t t0 = whisper_full_get_segment_t0(ctx, i);
        const int64_t t1 = whisper_full_get_segment_t1(ctx, i);

        data->current_segment = text;
        printf("[%s --> %s] %s\n",
               to_timestamp(t0).c_str(),
               to_timestamp(t1).c_str(),
               text);
    }
}

int transcribe_with_callbacks(const char * audio_file, const char * model_path) {
    // Initialize context
    struct whisper_context * ctx = whisper_init_from_file(model_path);
    if (!ctx) return 1;

    // Load audio
    std::vector<float> pcmf32;
    if (!read_wav_file(audio_file, pcmf32)) {
        whisper_free(ctx);
        return 1;
    }

    // Set up parameters with callbacks
    struct whisper_full_params wparams = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    wparams.progress_callback = whisper_progress_callback;
    wparams.new_segment_callback = whisper_new_segment_callback;

    CallbackData callback_data = {0, ""};
    wparams.progress_callback_user_data = &callback_data;
    wparams.new_segment_callback_user_data = &callback_data;

    // Run transcription
    if (whisper_full(ctx, wparams, pcmf32.data(), pcmf32.size()) != 0) {
        fprintf(stderr, "Transcription failed\n");
        whisper_free(ctx);
        return 1;
    }

    whisper_free(ctx);
    return 0;
}
```

## 🔄 Advanced Usage Patterns

### **Real-time Streaming Transcription**

```cpp
// Real-time audio streaming
class RealtimeTranscriber {
private:
    struct whisper_context * ctx;
    std::vector<float> audio_buffer;
    std::mutex buffer_mutex;
    std::thread processing_thread;
    bool running;

    // Circular buffer for audio
    static const int BUFFER_SIZE = 16000 * 30; // 30 seconds at 16kHz
    float audio_ring_buffer[BUFFER_SIZE];
    int buffer_write_pos = 0;
    int buffer_read_pos = 0;

public:
    RealtimeTranscriber(const char * model_path) : running(false) {
        ctx = whisper_init_from_file(model_path);
        if (!ctx) {
            throw std::runtime_error("Failed to initialize Whisper context");
        }
    }

    ~RealtimeTranscriber() {
        stop();
        if (ctx) whisper_free(ctx);
    }

    void start() {
        if (running) return;

        running = true;
        processing_thread = std::thread(&RealtimeTranscriber::processing_loop, this);
    }

    void stop() {
        running = false;
        if (processing_thread.joinable()) {
            processing_thread.join();
        }
    }

    void add_audio(const float * audio, int length) {
        std::lock_guard<std::mutex> lock(buffer_mutex);

        // Add audio to ring buffer
        for (int i = 0; i < length; ++i) {
            audio_ring_buffer[buffer_write_pos] = audio[i];
            buffer_write_pos = (buffer_write_pos + 1) % BUFFER_SIZE;
        }
    }

private:
    void processing_loop() {
        const int chunk_size = 16000 * 5; // 5 second chunks
        std::vector<float> chunk(chunk_size);

        while (running) {
            // Wait for enough audio data
            {
                std::lock_guard<std::mutex> lock(buffer_mutex);
                int available = (buffer_write_pos - buffer_read_pos + BUFFER_SIZE) % BUFFER_SIZE;

                if (available < chunk_size) {
                    std::this_thread::sleep_for(std::chrono::milliseconds(100));
                    continue;
                }

                // Read chunk from buffer
                for (int i = 0; i < chunk_size; ++i) {
                    chunk[i] = audio_ring_buffer[buffer_read_pos];
                    buffer_read_pos = (buffer_read_pos + 1) % BUFFER_SIZE;
                }
            }

            // Process chunk
            transcribe_chunk(chunk.data(), chunk_size);
        }
    }

    void transcribe_chunk(const float * audio, int length) {
        // Set up parameters for streaming
        struct whisper_full_params wparams = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
        wparams.no_context = true;  // Don't use previous context for streaming
        wparams.single_segment = true; // Process as single segment

        // Run transcription
        if (whisper_full(ctx, wparams, audio, length) == 0) {
            // Get result
            const int n_segments = whisper_full_n_segments(ctx);
            for (int i = 0; i < n_segments; ++i) {
                const char * text = whisper_full_get_segment_text(ctx, i);
                printf("[STREAM] %s\n", text);
            }
        }
    }
};
```

### **Language Detection and Translation**

```cpp
// Language detection and translation
int detect_and_translate(const char * audio_file, const char * model_path) {
    struct whisper_context * ctx = whisper_init_from_file(model_path);
    if (!ctx) return 1;

    // Load audio
    std::vector<float> pcmf32;
    if (!read_wav_file(audio_file, pcmf32)) {
        whisper_free(ctx);
        return 1;
    }

    // First pass: detect language
    struct whisper_full_params detect_params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    detect_params.language = nullptr; // Auto-detect
    detect_params.detect_language = true;
    detect_params.n_threads = 4;

    if (whisper_full(ctx, detect_params, pcmf32.data(), pcmf32.size()) != 0) {
        fprintf(stderr, "Language detection failed\n");
        whisper_free(ctx);
        return 1;
    }

    // Get detected language
    const int lang_id = whisper_full_lang_id(ctx);
    const char * detected_lang = whisper_lang_str(lang_id);
    const float lang_proba = whisper_full_lang_proba(ctx, lang_id);

    printf("Detected language: %s (probability: %.2f)\n", detected_lang, lang_proba);

    // Second pass: translate to English if not already English
    if (strcmp(detected_lang, "en") != 0) {
        struct whisper_full_params translate_params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
        translate_params.language = detected_lang;
        translate_params.translate = true; // Translate to English
        translate_params.n_threads = 4;

        if (whisper_full(ctx, translate_params, pcmf32.data(), pcmf32.size()) != 0) {
            fprintf(stderr, "Translation failed\n");
            whisper_free(ctx);
            return 1;
        }

        printf("Translation:\n");
        const int n_segments = whisper_full_n_segments(ctx);
        for (int i = 0; i < n_segments; ++i) {
            const char * text = whisper_full_get_segment_text(ctx, i);
            printf("%s\n", text);
        }
    }

    whisper_free(ctx);
    return 0;
}
```

### **Custom Vocabulary and Hotwords**

```cpp
// Using initial prompts and hotwords
int transcribe_with_prompt(const char * audio_file, const char * model_path, const char * prompt) {
    struct whisper_context * ctx = whisper_init_from_file(model_path);
    if (!ctx) return 1;

    // Load audio
    std::vector<float> pcmf32;
    if (!read_wav_file(audio_file, pcmf32)) {
        whisper_free(ctx);
        return 1;
    }

    // Convert prompt to tokens
    std::vector<whisper_token> prompt_tokens;
    if (prompt && strlen(prompt) > 0) {
        // Tokenize the prompt
        const int max_tokens = 256;
        prompt_tokens.resize(max_tokens);

        const int n_tokens = whisper_tokenize(ctx, prompt, prompt_tokens.data(), max_tokens);
        if (n_tokens < 0) {
            fprintf(stderr, "Failed to tokenize prompt\n");
            whisper_free(ctx);
            return 1;
        }

        prompt_tokens.resize(n_tokens);
    }

    // Set up parameters with prompt
    struct whisper_full_params wparams = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    wparams.initial_prompt_tokens = prompt_tokens.data();
    wparams.n_initial_prompt_tokens = prompt_tokens.size();
    wparams.language = "en";
    wparams.n_threads = 4;

    // Run transcription
    if (whisper_full(ctx, wparams, pcmf32.data(), pcmf32.size()) != 0) {
        fprintf(stderr, "Transcription failed\n");
        whisper_free(ctx);
        return 1;
    }

    // Print results
    const int n_segments = whisper_full_n_segments(ctx);
    for (int i = 0; i < n_segments; ++i) {
        const char * text = whisper_full_get_segment_text(ctx, i);
        printf("%s\n", text);
    }

    whisper_free(ctx);
    return 0;
}
```

## 🛠️ Error Handling and Resource Management

### **Comprehensive Error Handling**

```cpp
// Error handling wrapper
class WhisperErrorHandler {
public:
    enum ErrorCode {
        SUCCESS = 0,
        MODEL_LOAD_FAILED = 1,
        AUDIO_LOAD_FAILED = 2,
        TRANSCRIPTION_FAILED = 3,
        INVALID_PARAMETERS = 4,
        OUT_OF_MEMORY = 5,
        THREAD_ERROR = 6
    };

    struct WhisperResult {
        ErrorCode code;
        std::string message;
        std::string transcription;
        std::vector<std::string> segments;
        std::vector<std::pair<int64_t, int64_t>> timestamps;
    };

    static WhisperResult transcribe_with_error_handling(
        const std::string& audio_file,
        const std::string& model_path,
        const whisper_full_params& params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY)
    ) {
        WhisperResult result;
        result.code = SUCCESS;

        // Validate inputs
        if (audio_file.empty()) {
            result.code = INVALID_PARAMETERS;
            result.message = "Audio file path is empty";
            return result;
        }

        if (model_path.empty()) {
            result.code = INVALID_PARAMETERS;
            result.message = "Model path is empty";
            return result;
        }

        // Check file existence
        if (!file_exists(audio_file)) {
            result.code = AUDIO_LOAD_FAILED;
            result.message = "Audio file does not exist: " + audio_file;
            return result;
        }

        if (!file_exists(model_path)) {
            result.code = MODEL_LOAD_FAILED;
            result.message = "Model file does not exist: " + model_path;
            return result;
        }

        // Initialize Whisper
        struct whisper_context_params cparams = whisper_context_default_params();
        struct whisper_context * ctx = nullptr;

        try {
            ctx = whisper_init_from_file_with_params(model_path.c_str(), cparams);
            if (!ctx) {
                result.code = MODEL_LOAD_FAILED;
                result.message = "Failed to initialize Whisper context";
                return result;
            }

            // Load audio
            std::vector<float> pcmf32;
            if (!read_wav_file(audio_file.c_str(), pcmf32)) {
                result.code = AUDIO_LOAD_FAILED;
                result.message = "Failed to load audio file: " + audio_file;
                return result;
            }

            // Validate audio
            if (pcmf32.empty()) {
                result.code = AUDIO_LOAD_FAILED;
                result.message = "Audio file is empty or invalid";
                return result;
            }

            // Run transcription
            if (whisper_full(ctx, params, pcmf32.data(), pcmf32.size()) != 0) {
                result.code = TRANSCRIPTION_FAILED;
                result.message = "Transcription failed";
                return result;
            }

            // Extract results
            const int n_segments = whisper_full_n_segments(ctx);
            for (int i = 0; i < n_segments; ++i) {
                const char * text = whisper_full_get_segment_text(ctx, i);
                const int64_t t0 = whisper_full_get_segment_t0(ctx, i);
                const int64_t t1 = whisper_full_get_segment_t1(ctx, i);

                result.segments.push_back(text);
                result.timestamps.push_back({t0, t1});
            }

            result.transcription = join_segments(result.segments);

        } catch (const std::exception& e) {
            result.code = TRANSCRIPTION_FAILED;
            result.message = std::string("Exception during transcription: ") + e.what();
        } catch (...) {
            result.code = TRANSCRIPTION_FAILED;
            result.message = "Unknown error during transcription";
        }

        // Cleanup
        if (ctx) {
            whisper_free(ctx);
        }

        return result;
    }

private:
    static bool file_exists(const std::string& path) {
        std::ifstream f(path.c_str());
        return f.good();
    }

    static std::string join_segments(const std::vector<std::string>& segments) {
        std::stringstream ss;
        for (size_t i = 0; i < segments.size(); ++i) {
            if (i > 0) ss << " ";
            ss << segments[i];
        }
        return ss.str();
    }
};
```

## 🔧 Integration Patterns

### **C++ Application Integration**

```cpp
// C++ class wrapper
class WhisperTranscriber {
private:
    struct whisper_context * ctx;
    bool initialized;

public:
    WhisperTranscriber() : ctx(nullptr), initialized(false) {}

    ~WhisperTranscriber() {
        if (ctx) {
            whisper_free(ctx);
        }
    }

    bool initialize(const std::string& model_path) {
        if (initialized) return true;

        struct whisper_context_params cparams = whisper_context_default_params();
        ctx = whisper_init_from_file_with_params(model_path.c_str(), cparams);

        if (!ctx) {
            std::cerr << "Failed to initialize Whisper context" << std::endl;
            return false;
        }

        initialized = true;
        return true;
    }

    std::optional<std::string> transcribe(const std::vector<float>& audio, const whisper_full_params& params) {
        if (!initialized || !ctx) {
            std::cerr << "Whisper not initialized" << std::endl;
            return std::nullopt;
        }

        if (whisper_full(ctx, params, audio.data(), audio.size()) != 0) {
            std::cerr << "Transcription failed" << std::endl;
            return std::nullopt;
        }

        // Collect all segments
        std::stringstream result;
        const int n_segments = whisper_full_n_segments(ctx);
        for (int i = 0; i < n_segments; ++i) {
            const char * text = whisper_full_get_segment_text(ctx, i);
            if (i > 0) result << " ";
            result << text;
        }

        return result.str();
    }

    bool is_initialized() const {
        return initialized;
    }
};

// Usage example
int main() {
    WhisperTranscriber transcriber;

    if (!transcriber.initialize("models/ggml-base.bin")) {
        return 1;
    }

    // Load audio
    std::vector<float> audio;
    // ... load audio data ...

    // Configure parameters
    auto params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    params.language = "en";

    // Transcribe
    auto result = transcriber.transcribe(audio, params);
    if (result) {
        std::cout << "Transcription: " << *result << std::endl;
    }

    return 0;
}
```

### **C API Integration**

```c
// C API usage
#include <stdio.h>
#include <stdlib.h>
#include "whisper.h"

int main(int argc, char * argv[]) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <model> <wav>\n", argv[0]);
        return 1;
    }

    // Initialize
    struct whisper_context * ctx = whisper_init_from_file(argv[1]);
    if (!ctx) {
        fprintf(stderr, "Failed to load model\n");
        return 1;
    }

    // Load audio
    float * audio_data = NULL;
    int audio_length = 0;

    if (!load_audio_file(argv[2], &audio_data, &audio_length)) {
        fprintf(stderr, "Failed to load audio\n");
        whisper_free(ctx);
        return 1;
    }

    // Transcribe
    struct whisper_full_params params = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    params.language = "en";

    if (whisper_full(ctx, params, audio_data, audio_length) != 0) {
        fprintf(stderr, "Transcription failed\n");
        free(audio_data);
        whisper_free(ctx);
        return 1;
    }

    // Print results
    const int n_segments = whisper_full_n_segments(ctx);
    for (int i = 0; i < n_segments; ++i) {
        const char * text = whisper_full_get_segment_text(ctx, i);
        printf("%s\n", text);
    }

    // Cleanup
    free(audio_data);
    whisper_free(ctx);

    return 0;
}
```

## 🎯 Key Takeaways

1. **Context Management**: Proper initialization and cleanup of Whisper contexts
2. **Parameter Configuration**: Understanding sampling strategies, language detection, and translation
3. **Callback Integration**: Progress callbacks, segment callbacks, and custom logging
4. **Error Handling**: Comprehensive error handling for production applications
5. **Resource Management**: Memory management and threading considerations

## 🧪 Hands-On Exercise

**Estimated Time: 60 minutes**

1. **Basic Transcription**: Implement a simple command-line transcription tool
2. **Callback Integration**: Add progress callbacks and real-time segment output
3. **Language Detection**: Build a tool that auto-detects language and translates
4. **Error Handling**: Implement comprehensive error handling and recovery
5. **C++ Wrapper**: Create a C++ class wrapper for easier integration

---

**Ready for real-time streaming?** Continue to [Chapter 5: Real-Time Streaming](05-real-time-streaming.md)