---
layout: default
title: "Instructor Tutorial - Chapter 2: Pydantic Models"
nav_order: 2
has_children: false
parent: Instructor Tutorial
---

# Chapter 2: Crafting Effective Pydantic Models

> Design schemas that guide the model toward accurate, typed responses with minimal retries.

## Overview

Strong schemas reduce hallucinations and retries. This chapter shows how to design models, add rich field hints, constrain values, and compose reusable components.

## Field Design Basics

```python
from pydantic import BaseModel, Field
from typing import Literal

class Issue(BaseModel):
    title: str = Field(..., description="short, imperative")
    severity: Literal["low", "medium", "high"] = Field(
        ..., description="user impact and urgency"
    )
    component: str = Field(..., description="affected module")
    steps: list[str] = Field(default_factory=list, description="ordered reproduction steps")
```

- Use `Literal` to force discrete options.
- Add short, specific descriptions.
- Prefer `default_factory` for lists/dicts to avoid `None` handling.

## Constrained Types

```python
from pydantic import BaseModel, Field, HttpUrl, conint

class Link(BaseModel):
    label: str
    url: HttpUrl

class Article(BaseModel):
    title: str = Field(..., min_length=4, max_length=120)
    tags: list[str] = Field(default_factory=list, max_items=8)
    reading_time_min: conint(ge=1, le=60) = 5
    sources: list[Link] = Field(default_factory=list)
```

- `conint`, `confloat`, `HttpUrl`, `EmailStr` add guardrails.
- `max_items` hints the model to keep arrays tight.

## Nested Models and Composition

```python
class Contact(BaseModel):
    name: str
    email: str

class Company(BaseModel):
    name: str
    domain: str
    contacts: list[Contact]
```

- Compose smaller models for clarity.
- Nesting guides the LLM to produce structured hierarchies.

## Optional vs Required

```python
from typing import Optional

class Lead(BaseModel):
    name: str
    company: Optional[str] = None
    phone: Optional[str] = Field(None, description="E.164 format")
```

- Provide descriptions even for optional fields so the LLM knows when to fill them.

## Enums vs Literals

```python
from enum import Enum

class Channel(str, Enum):
    email = "email"
    sms = "sms"
    push = "push"
```

Enums improve readability and reuse across models.

## Putting It Together with Instructor

```python
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())

class SupportTicket(BaseModel):
    issue: Issue
    priority: Literal["p1", "p2", "p3"]
    contact: Contact

ticket = client.responses.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Report a login failure for acme.com"}],
    response_model=SupportTicket,
)
print(ticket)
```

Clear schemas drastically cut retries and make outputs stable across providers.

## Tips

- Keep descriptions short and directive (“use ISO date”, “array of 3 bullets”).
- Cap list lengths (`max_items`) to avoid verbose responses.
- Use `Literal`/`Enum` for finite choices; combine with short guidance.
- Reuse nested models; avoid giant, flat objects that are hard for LLMs to follow.

Next: add validation and retry logic to guarantee quality. 
