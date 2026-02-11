---
layout: default
title: "Chapter 6: ChatML and Tool Call Accounting"
nav_order: 6
parent: tiktoken Tutorial
---

# Chapter 6: ChatML and Tool Call Accounting

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
