---
layout: default
title: "Chapter 6: Voice Output"
nav_order: 6
parent: OpenAI Realtime Agents Tutorial
---

# Chapter 6: Voice Output

Voice output quality is primarily a timing and interaction problem. Good prosody helps, but responsiveness and interruption behavior matter more.

## Learning Goals

By the end of this chapter, you should be able to:

- design low-latency output streaming behavior
- handle barge-in cleanly without losing conversation continuity
- monitor core audio response metrics
- tune output policy for different use cases

## Output Pipeline

1. response deltas are generated
2. audio is synthesized/streamed
3. client buffers and plays frames
4. playback is interrupted or completed
5. session state is updated for next turn

## Voice UX Rules of Thumb

- prefer short, direct phrasing
- avoid dense list-heavy answers in speech mode
- announce long actions briefly before tool calls
- use natural checkpoint phrases for easier interruption

## Barge-In Behavior

When user speaks during playback:

- stop playback immediately
- mark current response state as interrupted
- prioritize next user input event path
- ensure transcript/state remains coherent after cutover

## Latency Targets (Product-Dependent)

| Metric | Why It Matters |
|:-------|:---------------|
| time to first audio | user perceived responsiveness |
| interruption stop latency | user sense of control |
| full response completion latency | overall task pacing |
| playback error rate | trust and reliability |

## Output Regression Signals

- rising interruption dissatisfaction despite stable model quality
- increased repeated-user prompts ("hello?", "are you there?")
- higher manual retry rates for basic interactions
- audible clipping or stutter under normal network conditions

## Source References

- [OpenAI Realtime Guide](https://platform.openai.com/docs/guides/realtime)
- [openai/openai-realtime-agents Repository](https://github.com/openai/openai-realtime-agents)

## Summary

You now understand how to tune voice output for perceived speed, clarity, and user control.

Next: [Chapter 7: Advanced Patterns](07-advanced-patterns.md)
