---
layout: default
title: "Instructor Tutorial - Chapter 5: Streaming"
nav_order: 5
has_children: false
parent: Instructor Tutorial
---

# Chapter 5: Streaming Structured Outputs

> Stream partial objects for faster UX while keeping schema guarantees.

## Overview

Instructor can stream partial responses that are incrementally validated against your schema. This improves perceived latency and lets you render progressive results (e.g., bullets or sections as they arrive).

## Basic Streaming Example

```python
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

client = instructor.from_openai(OpenAI())

class Idea(BaseModel):
    title: str
    blurb: str = Field(..., max_length=140)

stream = client.responses.stream(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Generate 3 marketing ideas for a note-taking app"}],
    response_model=list[Idea],
)

for partial in stream:
    print("partial:", partial)

ideas = stream.get_final_response()
print("final:", ideas)
```

- `responses.stream` yields partial objects as they are decoded.
- `get_final_response()` returns the validated final object.

## Rendering in a Web App

```python
# FastAPI skeleton
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

@app.post("/ideas")
async def ideas():
    stream = client.responses.stream(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Give 5 snack ideas"}],
        response_model=list[Idea],
    )

    async def event_source():
        for partial in stream:
            yield f"data: {json.dumps(partial.model_dump())}\n\n"
        yield f"data: {json.dumps(stream.get_final_response().model_dump())}\n\n"

    return StreamingResponse(event_source(), media_type="text/event-stream")
```

Use Server-Sent Events (SSE) or WebSockets to push partial objects to the UI.

## Tips for Stable Streaming

- Keep models concise; large schemas increase latency and validation cost.
- Stream lists of small objects rather than one giant object.
- Add `max_items` to avoid unbounded growth during streaming.
- If partials flicker in the UI, debounce or buffer before rendering.

Next: switch providers without rewriting schemas. 
