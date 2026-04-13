---
layout: default
title: "Chapter 8: Integration Examples"
nav_order: 8
parent: OpenAI Python SDK Tutorial
---


# Chapter 8: Integration Examples

Welcome to **Chapter 8: Integration Examples**. In this part of **OpenAI Python SDK Tutorial: Production API Patterns**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter maps core SDK features to service-level integration patterns.

## Example 1: FastAPI Summarization Endpoint

```python
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
client = OpenAI()

@app.post("/summarize")
def summarize(payload: dict):
    text = payload.get("text", "")
    resp = client.responses.create(
        model="gpt-5.2",
        input=f"Summarize in 3 bullet points:\n\n{text}",
    )
    return {"summary": resp.output_text, "request_id": resp.id}
```

## Example 2: Retrieval-Enhanced Endpoint

- retrieve top-k context from embeddings index
- construct compact context block
- generate answer with citation fields
- return both answer and source metadata

## Example 3: Tool-Gated Action Endpoint

- classify requested action risk
- require explicit confirmation for destructive operations
- run tool with bounded timeout
- log inputs and outputs for audit

## Final Launch Checklist

- contract tests for request/response schemas
- regression eval set for output quality
- budget alerts and rate-limit handling
- incident runbook for degraded provider behavior

## Final Summary

You now have an end-to-end blueprint for shipping Python SDK integrations that are reliable, observable, and migration-ready.

Related:
- [tiktoken Tutorial](../tiktoken-tutorial/)
- [OpenAI Realtime Agents Tutorial](../openai-realtime-agents-tutorial/)
- [OpenAI Whisper Tutorial](../openai-whisper-tutorial/)

## Source Code Walkthrough

### `examples/audio.py`

The `main` function in [`examples/audio.py`](https://github.com/openai/openai-python/blob/HEAD/examples/audio.py) handles a key part of this chapter's functionality:

```py


def main() -> None:
    # Create text-to-speech audio file
    with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input="the quick brown fox jumped over the lazy dogs",
    ) as response:
        response.stream_to_file(speech_file_path)

    # Create transcription from audio file
    transcription = openai.audio.transcriptions.create(
        model="whisper-1",
        file=speech_file_path,
    )
    print(transcription.text)

    # Create translation from audio file
    translation = openai.audio.translations.create(
        model="whisper-1",
        file=speech_file_path,
    )
    print(translation.text)


if __name__ == "__main__":
    main()

```

This function is important because it defines how OpenAI Python SDK Tutorial: Production API Patterns implements the patterns covered in this chapter.

### `examples/uploads.py`

The `from_disk` function in [`examples/uploads.py`](https://github.com/openai/openai-python/blob/HEAD/examples/uploads.py) handles a key part of this chapter's functionality:

```py


def from_disk() -> None:
    print("uploading file from disk")

    upload = client.uploads.upload_file_chunked(
        file=file,
        mime_type="txt",
        purpose="batch",
    )
    rich.print(upload)


def from_in_memory() -> None:
    print("uploading file from memory")

    # read the data into memory ourselves to simulate
    # it coming from somewhere else
    data = file.read_bytes()
    filename = "my_file.txt"

    upload = client.uploads.upload_file_chunked(
        file=data,
        filename=filename,
        bytes=len(data),
        mime_type="txt",
        purpose="batch",
    )
    rich.print(upload)


if "memory" in sys.argv:
```

This function is important because it defines how OpenAI Python SDK Tutorial: Production API Patterns implements the patterns covered in this chapter.

### `examples/uploads.py`

The `from_in_memory` function in [`examples/uploads.py`](https://github.com/openai/openai-python/blob/HEAD/examples/uploads.py) handles a key part of this chapter's functionality:

```py


def from_in_memory() -> None:
    print("uploading file from memory")

    # read the data into memory ourselves to simulate
    # it coming from somewhere else
    data = file.read_bytes()
    filename = "my_file.txt"

    upload = client.uploads.upload_file_chunked(
        file=data,
        filename=filename,
        bytes=len(data),
        mime_type="txt",
        purpose="batch",
    )
    rich.print(upload)


if "memory" in sys.argv:
    from_in_memory()
else:
    from_disk()

```

This function is important because it defines how OpenAI Python SDK Tutorial: Production API Patterns implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[main]
    B[from_disk]
    C[from_in_memory]
    A --> B
    B --> C
```
