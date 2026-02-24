---
layout: default
title: "Chapter 5: Permissions and Approval Workflow"
nav_order: 5
parent: HAPI Tutorial
---

# Chapter 5: Permissions and Approval Workflow

Welcome to **Chapter 5: Permissions and Approval Workflow**. In this part of **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Remote approvals are the core safety boundary when agents request actions.

## Approval Event Flow

1. agent emits permission request
2. CLI forwards request to hub
3. hub stores and broadcasts to PWA/Telegram
4. operator approves/denies
5. decision returns to active session

## Policy Matrix

| Request Type | Recommended Policy |
|:-------------|:-------------------|
| scoped file edits | approve with diff visibility |
| command execution | require explicit command preview |
| destructive/system-wide actions | deny by default |

## Operational Controls

- enforce timeout for unresolved approvals
- require request metadata (target file/command/context)
- retain immutable approval logs for audit and incident review

## Summary

You now have a governance model for remote permission handling in HAPI.

Next: [Chapter 6: PWA, Telegram, and Extensions](06-pwa-telegram-and-extensions.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for core abstractions in this chapter so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Permissions and Approval Workflow` as an operating subsystem inside **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around execution and reliability details as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Permissions and Approval Workflow` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `core component`.
2. **Input normalization**: shape incoming data so `execution layer` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `state model`.
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

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Remote Access and Networking](04-remote-access-and-networking.md)
- [Next Chapter: Chapter 6: PWA, Telegram, and Extensions](06-pwa-telegram-and-extensions.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
