---
layout: default
title: "Chapter 6: Model Strategy and Remote Server Mode"
nav_order: 6
parent: AgenticSeek Tutorial
---


# Chapter 6: Model Strategy and Remote Server Mode

Welcome to **Chapter 6: Model Strategy and Remote Server Mode**. In this part of **AgenticSeek Tutorial: Local-First Autonomous Agent Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter helps you select model-provider strategy based on cost, latency, and privacy constraints.

## Learning Goals

- compare local model mode vs API mode vs self-hosted server mode
- understand tradeoffs for hardware-constrained environments
- configure remote server operation cleanly
- prevent common provider-mode misconfiguration

## Provider Modes

- local mode (`is_local=True`): best for privacy and cost control
- API mode (`is_local=False`): best for limited local hardware
- server mode (`provider_name=server`): best when model runs on separate machine

## Remote Server Pattern

For server mode, run the LLM server process on remote host, then set:

```ini
[MAIN]
is_local = False
provider_name = server
provider_model = deepseek-r1:70b
provider_server_address = http://<server-ip>:3333
```

This pattern keeps interaction device lightweight while preserving self-hosted model control.

## Decision Matrix

| Constraint | Recommended Mode |
|:-----------|:-----------------|
| Strong privacy + enough GPU | Local mode |
| Limited local hardware | API mode |
| Strong privacy + remote GPU server | Server mode |

## Source References

- [README Local Provider Setup](https://github.com/Fosowl/agenticSeek/blob/main/README.md#setup-for-running-llm-locally-on-your-machine)
- [README API Provider Setup](https://github.com/Fosowl/agenticSeek/blob/main/README.md#setup-to-run-with-an-api)
- [LLM Server Directory](https://github.com/Fosowl/agenticSeek/tree/main/llm_server)

## Summary

You now have a clear provider strategy aligned to hardware and governance needs.

Next: [Chapter 7: Troubleshooting and Reliability Playbook](07-troubleshooting-and-reliability-playbook.md)

## Source Code Walkthrough

### `sources/providers.py` and `llm_server/app.py`

Model strategy and remote server mode are defined across two files. [`sources/providers.py`](https://github.com/Fosowl/agenticSeek/blob/HEAD/sources/providers.py) implements the provider abstraction that lets users switch between local models and remote endpoints. [`llm_server/app.py`](https://github.com/Fosowl/agenticSeek/blob/HEAD/llm_server/app.py) is the Flask server that exposes a local model as an HTTP API — the remote server mode described in Chapter 6. Together they define the full model strategy: local-only, API-backed, or self-hosted remote.