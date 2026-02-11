---
layout: default
title: "Chapter 5: Function Calling"
nav_order: 5
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 5: Function Calling

Tool execution lets realtime agents act on live data during voice interactions.

## Define Tools

```ts
const tools = [
  {
    type: "function",
    name: "get_weather",
    description: "Get current weather by city",
    parameters: {
      type: "object",
      properties: { city: { type: "string" } },
      required: ["city"],
    },
  },
];
```

## Tool Execution Loop

1. Receive tool-call event.
2. Validate arguments.
3. Execute server-side function.
4. Send tool result event.
5. Resume assistant response.

## Safety Rules

- Never trust raw tool arguments.
- Enforce allowlisted operations.
- Set execution timeouts and retries.

## Summary

You can now run real-time function calls safely in voice sessions.

Next: [Chapter 6: Voice Output](06-voice-output.md)
