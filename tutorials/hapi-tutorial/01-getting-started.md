---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: HAPI Tutorial
---

# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gets HAPI installed and verifies a full terminal-to-mobile control loop.

## Prerequisites

| Requirement | Purpose |
|:------------|:--------|
| Claude/Codex/Gemini/OpenCode CLI | agent runtime HAPI wraps |
| npm/Homebrew | HAPI install path |
| phone/browser access | remote approvals and messaging |

## Install and Start

```bash
npm install -g @twsxtd/hapi
hapi hub --relay
hapi
```

`hapi server` is supported as a hub alias.

## First Session Validation

1. hub prints URL + QR code
2. login using generated access token
3. session appears in UI
4. send a message from phone/web and observe terminal response
5. verify permission prompt can be approved remotely

## Initial Troubleshooting

- ensure underlying agent CLI is installed and authenticated
- confirm `HAPI_API_URL`/`CLI_API_TOKEN` when hub is not localhost
- verify relay/tunnel reachability and TLS path

## Summary

You now have a working HAPI baseline with remote control enabled.

Next: [Chapter 2: System Architecture](02-system-architecture.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `hapi`, `install`, `twsxtd` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started` as an operating subsystem inside **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `relay` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `hapi`.
2. **Input normalization**: shape incoming data so `install` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `twsxtd`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [HAPI Repository](https://github.com/tiann/hapi)
  Why it matters: authoritative reference on `HAPI Repository` (github.com).
- [HAPI Releases](https://github.com/tiann/hapi/releases)
  Why it matters: authoritative reference on `HAPI Releases` (github.com).
- [HAPI Docs](https://hapi.run)
  Why it matters: authoritative reference on `HAPI Docs` (hapi.run).

Suggested trace strategy:
- search upstream code for `hapi` and `install` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: System Architecture](02-system-architecture.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
