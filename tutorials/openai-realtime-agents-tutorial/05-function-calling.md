---
layout: default
title: "Chapter 5: Function Calling"
nav_order: 5
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 5: Function Calling

Tooling is where realtime agents become operationally useful.

## Function-Call Workflow

1. model emits tool request with arguments
2. app validates and executes tool logic
3. tool result is returned to conversation
4. model synthesizes user-facing response

## Safety Requirements

Before executing any tool:

- validate schema and semantic constraints
- apply authorization checks
- enforce timeout budgets
- classify side-effect risk level

## Realtime-Specific Considerations

- tool latency should be surfaced in UX (for example, short acknowledgments)
- long-running tools need status updates or fallback paths
- partial results can reduce perceived latency when safe

## Structured Return Shape

Always return stable tool payloads.

```json
{
  "status": "ok",
  "data": {"order_id": "123", "state": "shipped"},
  "confidence": 0.98
}
```

This improves downstream response reliability and simplifies auditing.

## Anti-Patterns

- returning unstructured free text from tools
- giving tools direct access to unrestricted resources
- silently swallowing tool errors

## Summary

You now have a dependable model for real-time tool use and response synthesis.

Next: [Chapter 6: Voice Output](06-voice-output.md)
