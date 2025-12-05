---
layout: default
title: "Instructor Tutorial - Chapter 3: Validation & Retries"
nav_order: 3
has_children: false
parent: Instructor Tutorial
---

# Chapter 3: Validation, Errors, and Retries

> Enforce data quality with Pydantic validation, custom errors, and automatic retries.

## Overview

Instructor validates LLM outputs against your schema. Failed validations trigger retries with corrective instructions. You can add custom validators and control retry behavior for stricter guarantees.

## Built-in Validation & Retries

```python
from pydantic import BaseModel, Field, ValidationError
import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())

class Person(BaseModel):
    name: str = Field(..., min_length=3)
    age: int = Field(..., ge=0, le=120)
    email: str | None = Field(None, description="valid email if provided")

try:
    person = client.responses.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Return a person, age must be <=120"}],
        response_model=Person,
        max_retries=3,
    )
    print(person)
except ValidationError as e:
    print("Validation failed:", e)
```

- `max_retries` controls how many times Instructor will re-prompt with validation errors.
- `ValidationError` surfaces the schema violations if retries fail.

## Custom Validation with `field_validator`

```python
from pydantic import field_validator

class Survey(BaseModel):
    satisfaction: int = Field(..., ge=1, le=5)
    comment: str

    @field_validator("comment")
    @classmethod
    def must_be_concise(cls, v):
        if len(v.split()) > 50:
            raise ValueError("comment too long; keep under 50 words")
        return v
```

Custom validators add domain rules the LLM must satisfy.

## Handling Partial Failures

Sometimes you want partial success with details on failures.

```python
class Product(BaseModel):
    name: str
    price: float = Field(..., ge=0)

class Catalog(BaseModel):
    products: list[Product]
```

If a single product fails validation, Instructor retries with error context. For large lists, consider capping `max_items` or splitting the request.

## Retry Feedback Prompts

Instructor automatically sends validation errors back to the LLM. You can add explicit guidance in the original prompt:

```
System: Follow the schema exactly. If a value is unclear, choose a sensible default rather than inventing data.
```

## Logging Validation Errors

Capture errors for monitoring and debugging:

```python
import logging
logger = logging.getLogger("instructor")

try:
    # call client.responses.create(...)
    pass
except ValidationError as e:
    logger.warning("Schema violation: %s", e)
```

## Tips

- Use constraints (`min_length`, `ge`, `Literal`) to reduce ambiguity.
- Keep `max_retries` small (1–3) to control costs; improve the schema before raising it.
- Add short field descriptions so retry hints are clear to the model.

Next: model complex, nested structures while keeping outputs stable. 
