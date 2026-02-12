---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Composio Tutorial
---

# Chapter 1: Getting Started

This chapter establishes a fast path to running a first Composio-backed agent with real toolkit actions.

## Learning Goals

- launch a first end-to-end session with authenticated tool use
- select an initial provider path without over-optimizing
- validate user scoping and session behavior early
- capture a minimal production-oriented baseline

## Fast Start Loop

1. follow the [Quickstart](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/quickstart.mdx)
2. create one test `user_id` and session
3. run a bounded task using a single toolkit (for example GitHub or Gmail)
4. complete authentication via Connect Link when prompted
5. verify response quality, tool-call behavior, and traceability

## Baseline Checklist

| Check | Expected Outcome |
|:------|:-----------------|
| session creation | stable session object with tool access |
| auth prompt | connect flow appears when required |
| tool execution | returns structured response and useful metadata |
| repeatability | same task behaves consistently across runs |

## Source References

- [Quickstart](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/quickstart.mdx)
- [README](https://github.com/ComposioHQ/composio/blob/next/README.md)

## Summary

You now have a practical starting baseline for iterative Composio adoption.

Next: [Chapter 2: Sessions, Meta Tools, and User Scoping](02-sessions-meta-tools-and-user-scoping.md)
