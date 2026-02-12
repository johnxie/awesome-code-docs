---
layout: default
title: "Chapter 5: Sessions, Memory, and Context Management"
nav_order: 5
parent: ADK Python Tutorial
---

# Chapter 5: Sessions, Memory, and Context Management

This chapter focuses on context durability and state boundaries.

## Learning Goals

- separate session state from long-term memory
- choose storage services based on workload needs
- control context growth with compaction patterns
- design memory usage for predictable outcomes

## Practical Guidance

- use session services for per-conversation event history
- use memory services for cross-session recall
- monitor compaction behavior to preserve critical facts
- define retention and governance policies early

## Source References

- [ADK AGENTS.md: Sessions and Memory](https://github.com/google/adk-python/blob/main/AGENTS.md)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Deploy Docs](https://google.github.io/adk-docs/deploy/)

## Summary

You can now reason about short-term context and long-term recall without mixing concerns.

Next: [Chapter 6: Evaluation, Debugging, and Quality Gates](06-evaluation-debugging-and-quality-gates.md)
