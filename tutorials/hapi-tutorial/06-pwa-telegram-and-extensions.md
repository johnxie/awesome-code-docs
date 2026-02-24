---
layout: default
title: "Chapter 6: PWA, Telegram, and Extensions"
nav_order: 6
parent: HAPI Tutorial
---

# Chapter 6: PWA, Telegram, and Extensions

Welcome to **Chapter 6: PWA, Telegram, and Extensions**. In this part of **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


HAPI supports multiple control surfaces so users can choose the right experience for context and urgency.

## Client Surface Comparison

| Surface | Best For |
|:--------|:---------|
| PWA | full mobile/desktop remote session control |
| Telegram Mini App | fast approvals and notification-first workflow |
| terminal + runner | machine-level orchestration and spawning |

## PWA Operations

- install as home-screen app for fast access
- use notification permissions for approval alerts
- rely on cached UI for degraded connectivity scenarios

## Extension Opportunities

Use runner + machine identities to route new sessions to specific hosts based on performance, policy, or ownership.

## Summary

You can now align HAPI interfaces with operator roles and team workflow needs.

Next: [Chapter 7: Configuration and Security](07-configuration-and-security.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for core abstractions in this chapter so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: PWA, Telegram, and Extensions` as an operating subsystem inside **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around execution and reliability details as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: PWA, Telegram, and Extensions` usually follows a repeatable control path:

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
- [Previous Chapter: Chapter 5: Permissions and Approval Workflow](05-permissions-and-approval-workflow.md)
- [Next Chapter: Chapter 7: Configuration and Security](07-configuration-and-security.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
