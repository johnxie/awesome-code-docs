---
layout: default
title: "Chapter 6: ChatML and Tool Call Accounting"
nav_order: 6
parent: tiktoken Tutorial
---


# Chapter 6: ChatML and Tool Call Accounting

Welcome to **Chapter 6: ChatML and Tool Call Accounting**. In this part of **tiktoken Tutorial: OpenAI Token Encoding & Optimization**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Accurate token accounting for chat and tools is essential for reliability and cost predictability.

## Where Underestimation Happens

Teams often count only user-visible text and miss:

- role/message wrapper overhead
- tool schema tokens
- serialized tool arguments/results
- retry-induced duplicate token spend

## Accounting Strategy

1. tokenize each message with the exact target encoding
2. add fixed wrapper overhead expected by your request format
3. account for tool payloads separately
4. include response-token guardband for retries/replans

## Example Helper

```python
def estimate_chat_tokens(messages, encoding, fixed_overhead=0):
    total = fixed_overhead
    for m in messages:
        total += len(encoding.encode(m.get("content", "")))
    return total
```

For tool flows, create separate counters for:

- tool call request payload
- tool response payload
- assistant synthesis after tool result

## Operational Use

- preflight estimate before API call
- reject or compress if over budget
- log estimate vs actual for calibration

## Summary

You can now estimate chat/tool token usage with fewer hidden-cost surprises.

Next: [Chapter 7: Multilingual Tokenization](07-multilingual-tokenization.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `total`, `messages`, `encoding` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: ChatML and Tool Call Accounting` as an operating subsystem inside **tiktoken Tutorial: OpenAI Token Encoding & Optimization**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `fixed_overhead`, `estimate_chat_tokens`, `encode` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: ChatML and Tool Call Accounting` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `total`.
2. **Input normalization**: shape incoming data so `messages` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `encoding`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [tiktoken repository](https://github.com/openai/tiktoken)
  Why it matters: authoritative reference on `tiktoken repository` (github.com).

Suggested trace strategy:
- search upstream code for `total` and `messages` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](README.md)
- [Previous Chapter: Chapter 5: Optimization Strategies](05-optimization-strategies.md)
- [Next Chapter: Chapter 7: Multilingual Tokenization](07-multilingual-tokenization.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `tiktoken/model.py`

The `encoding_for_model` function in [`tiktoken/model.py`](https://github.com/openai/tiktoken/blob/HEAD/tiktoken/model.py) handles a key part of this chapter's functionality:

```py


def encoding_for_model(model_name: str) -> Encoding:
    """Returns the encoding used by a model.

    Raises a KeyError if the model name is not recognised.
    """
    return get_encoding(encoding_name_for_model(model_name))

```

This function is important because it defines how tiktoken Tutorial: OpenAI Token Encoding & Optimization implements the patterns covered in this chapter.

### `scripts/wheel_download.py`

The `download_artifacts` function in [`scripts/wheel_download.py`](https://github.com/openai/tiktoken/blob/HEAD/scripts/wheel_download.py) handles a key part of this chapter's functionality:

```py


def download_artifacts(token, owner, repo, run_id, output_dir):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

    # Get list of artifacts
    artifacts_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
    response = requests.get(artifacts_url, headers=headers)
    response.raise_for_status()
    artifacts = response.json()["artifacts"]

    if not artifacts:
        print(f"No artifacts found for run ID: {run_id}")
        return

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(artifacts)} artifacts")
    for artifact in artifacts:
        name = artifact["name"]
        download_url = artifact["archive_download_url"]

        print(f"Downloading {name}...")

        response = requests.get(download_url, headers=headers, stream=True)
        response.raise_for_status()

        temp_zip = output_dir / f"{name}.zip"
        with open(temp_zip, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
```

This function is important because it defines how tiktoken Tutorial: OpenAI Token Encoding & Optimization implements the patterns covered in this chapter.

### `scripts/redact.py`

The `redact_file` function in [`scripts/redact.py`](https://github.com/openai/tiktoken/blob/HEAD/scripts/redact.py) handles a key part of this chapter's functionality:

```py


def redact_file(path: Path, dry_run: bool) -> None:
    if not path.exists() or path.is_dir():
        return

    text = path.read_text()
    if not text:
        return

    first_line = text.splitlines()[0]
    if "redact" in first_line:
        if not dry_run:
            path.unlink()
        print(f"Deleted {path}")
        return

    pattern = "|".join(
        r" *" + re.escape(x)
        for x in [
            "# ===== redact-beg =====\n",
            "# ===== redact-end =====\n",
            "<!--- redact-beg -->\n",
            "<!--- redact-end -->\n",
        ]
    )

    if re.search(pattern, text):
        redacted_text = "".join(re.split(pattern, text)[::2])
        if not dry_run:
            path.write_text(redacted_text)
        print(f"Redacted {path}")
```

This function is important because it defines how tiktoken Tutorial: OpenAI Token Encoding & Optimization implements the patterns covered in this chapter.

### `scripts/redact.py`

The `redact` function in [`scripts/redact.py`](https://github.com/openai/tiktoken/blob/HEAD/scripts/redact.py) handles a key part of this chapter's functionality:

```py


def redact_file(path: Path, dry_run: bool) -> None:
    if not path.exists() or path.is_dir():
        return

    text = path.read_text()
    if not text:
        return

    first_line = text.splitlines()[0]
    if "redact" in first_line:
        if not dry_run:
            path.unlink()
        print(f"Deleted {path}")
        return

    pattern = "|".join(
        r" *" + re.escape(x)
        for x in [
            "# ===== redact-beg =====\n",
            "# ===== redact-end =====\n",
            "<!--- redact-beg -->\n",
            "<!--- redact-end -->\n",
        ]
    )

    if re.search(pattern, text):
        redacted_text = "".join(re.split(pattern, text)[::2])
        if not dry_run:
            path.write_text(redacted_text)
        print(f"Redacted {path}")
```

This function is important because it defines how tiktoken Tutorial: OpenAI Token Encoding & Optimization implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[encoding_for_model]
    B[download_artifacts]
    C[redact_file]
    D[redact]
    E[main]
    A --> B
    B --> C
    C --> D
    D --> E
```
