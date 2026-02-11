---
layout: default
title: "Chapter 5: Function Calling"
nav_order: 5
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 5: Function Calling

Function calling is where realtime agents move from conversation to action. It must be fast, safe, and auditable.

## Learning Goals

By the end of this chapter, you should be able to:

- implement a reliable tool-call lifecycle
- enforce schema and authorization checks before execution
- design robust error and timeout handling for realtime UX
- return structured outputs that improve downstream response quality

## Tool-Call Lifecycle

1. model emits tool request with arguments
2. gateway validates schema and authorization
3. tool executes with timeout and retry policy
4. structured result (or structured error) returns to session
5. assistant synthesizes user-facing response

## Tool Gateway Requirements

| Requirement | Purpose |
|:------------|:--------|
| strict argument validation | prevents malformed or unsafe calls |
| auth and policy checks | enforces user/tenant permissions |
| timeout budgeting | protects responsiveness |
| idempotency keys | reduces duplicate side effects on retries |
| structured logging | supports forensic debugging |

## Realtime-Specific UX Considerations

- acknowledge long-running tools immediately
- stream progress where possible
- provide deterministic fallback when tool backend is unavailable
- never leave the user without a completion/error state

## Recommended Result Contract

```json
{
  "status": "ok",
  "data": {"order_id": "123", "state": "shipped"},
  "confidence": 0.98,
  "trace_id": "tool-req-abc"
}
```

For errors, keep an explicit shape (`status`, `error_code`, `message`, `retryable`).

## High-Risk Anti-Patterns

- unrestricted tool access from model-generated arguments
- free-form text outputs instead of typed result envelopes
- silent tool failures without user-visible recovery
- long retries that block turn transitions

## Source References

- [openai/openai-realtime-agents Repository](https://github.com/openai/openai-realtime-agents)
- [OpenAI Realtime Guide](https://platform.openai.com/docs/guides/realtime)

## Summary

You now have a production-safe tool-calling blueprint for realtime agents with clear reliability and security controls.

Next: [Chapter 6: Voice Output](06-voice-output.md)
