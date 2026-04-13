---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenAI Python SDK Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **OpenAI Python SDK Tutorial: Production API Patterns**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gets you to a stable baseline with Responses API-first code.

## Install and Configure

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai
export OPENAI_API_KEY="your_api_key_here"
```

## First Responses API Call

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.2",
    input="Summarize why idempotency matters in API design in 3 bullets."
)

print(response.output_text)
```

## Async Variant

```python
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI()
    resp = await client.responses.create(
        model="gpt-5.2",
        input="Give 3 tips for reliable background jobs."
    )
    print(resp.output_text)

asyncio.run(main())
```

## Baseline Production Controls

- set explicit client timeouts
- capture request IDs in logs
- keep secrets out of source control
- fail fast on invalid configuration

## Summary

You now have a working SDK setup with both sync and async Responses API calls.

Next: [Chapter 2: Chat Completions](02-chat-completions.md)

## Source Code Walkthrough

### `scripts/detect-breaking-changes.py`

The `public_members` function in [`scripts/detect-breaking-changes.py`](https://github.com/openai/openai-python/blob/HEAD/scripts/detect-breaking-changes.py) handles a key part of this chapter's functionality:

```py


def public_members(obj: griffe.Object | griffe.Alias) -> dict[str, griffe.Object | griffe.Alias]:
    if isinstance(obj, griffe.Alias):
        # ignore imports for now, they're technically part of the public API
        # but we don't have good preventative measures in place to prevent
        # changing them
        return {}

    return {name: value for name, value in obj.all_members.items() if not name.startswith("_")}


def find_breaking_changes(
    new_obj: griffe.Object | griffe.Alias,
    old_obj: griffe.Object | griffe.Alias,
    *,
    path: list[str],
) -> Iterator[Text | str]:
    new_members = public_members(new_obj)
    old_members = public_members(old_obj)

    for name, old_member in old_members.items():
        if isinstance(old_member, griffe.Alias) and len(path) > 2:
            # ignore imports in `/types/` for now, they're technically part of the public API
            # but we don't have good preventative measures in place to prevent changing them
            continue

        new_member = new_members.get(name)
        if new_member is None:
            cls_name = old_member.__class__.__name__
            yield Text(f"({cls_name})", style=Style(color="rgb(119, 119, 119)"))
            yield from [" " for _ in range(10 - len(cls_name))]
```

This function is important because it defines how OpenAI Python SDK Tutorial: Production API Patterns implements the patterns covered in this chapter.

### `scripts/detect-breaking-changes.py`

The `find_breaking_changes` function in [`scripts/detect-breaking-changes.py`](https://github.com/openai/openai-python/blob/HEAD/scripts/detect-breaking-changes.py) handles a key part of this chapter's functionality:

```py


def find_breaking_changes(
    new_obj: griffe.Object | griffe.Alias,
    old_obj: griffe.Object | griffe.Alias,
    *,
    path: list[str],
) -> Iterator[Text | str]:
    new_members = public_members(new_obj)
    old_members = public_members(old_obj)

    for name, old_member in old_members.items():
        if isinstance(old_member, griffe.Alias) and len(path) > 2:
            # ignore imports in `/types/` for now, they're technically part of the public API
            # but we don't have good preventative measures in place to prevent changing them
            continue

        new_member = new_members.get(name)
        if new_member is None:
            cls_name = old_member.__class__.__name__
            yield Text(f"({cls_name})", style=Style(color="rgb(119, 119, 119)"))
            yield from [" " for _ in range(10 - len(cls_name))]
            yield f" {'.'.join(path)}.{name}"
            yield "\n"
            continue

        yield from find_breaking_changes(new_member, old_member, path=[*path, name])


def main() -> None:
    try:
        against_ref = sys.argv[1]
```

This function is important because it defines how OpenAI Python SDK Tutorial: Production API Patterns implements the patterns covered in this chapter.

### `scripts/detect-breaking-changes.py`

The `main` function in [`scripts/detect-breaking-changes.py`](https://github.com/openai/openai-python/blob/HEAD/scripts/detect-breaking-changes.py) handles a key part of this chapter's functionality:

```py


def main() -> None:
    try:
        against_ref = sys.argv[1]
    except IndexError as err:
        raise RuntimeError("You must specify a base ref to run breaking change detection against") from err

    package = griffe.load(
        "openai",
        search_paths=[Path(__file__).parent.parent.joinpath("src")],
    )
    old_package = griffe.load_git(
        "openai",
        ref=against_ref,
        search_paths=["src"],
    )
    assert isinstance(package, griffe.Module)
    assert isinstance(old_package, griffe.Module)

    output = list(find_breaking_changes(package, old_package, path=["openai"]))
    if output:
        rich.print(Text("Breaking changes detected!", style=Style(color="rgb(165, 79, 87)")))
        rich.print()

        for text in output:
            rich.print(text, end="")

        sys.exit(1)


main()
```

This function is important because it defines how OpenAI Python SDK Tutorial: Production API Patterns implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[public_members]
    B[find_breaking_changes]
    C[main]
    A --> B
    B --> C
```
