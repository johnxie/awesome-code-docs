---
layout: default
title: "Chapter 6: ChatML and Tool Call Accounting"
nav_order: 6
parent: tiktoken Tutorial
---

# Chapter 6: ChatML and Tool Call Accounting

This chapter covers reliable token accounting for chat messages and tool-call payloads.

## Message Accounting Pattern

- count tokens per message role (`system`, `user`, `assistant`)
- include hidden scaffolding overhead in estimates
- budget separately for tool arguments and tool results

## Practical Rule

Always estimate using the exact model encoding and message format you will send.

## Example

```python
def estimate_chat_tokens(messages, enc):
    return sum(len(enc.encode(m["content"])) for m in messages)
```

## Summary

You can now avoid underestimating token cost in chat-tool workflows.

Next: [Chapter 7: Multilingual Tokenization](07-multilingual-tokenization.md)
