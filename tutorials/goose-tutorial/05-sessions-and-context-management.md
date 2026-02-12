---
layout: default
title: "Chapter 5: Sessions and Context Management"
nav_order: 5
parent: Goose Tutorial
---

# Chapter 5: Sessions and Context Management

This chapter explains how Goose keeps long-running workflows productive without losing context quality.

## Learning Goals

- manage session lifecycle and naming cleanly
- use context compaction and strategies intentionally
- control runaway loops with max-turn governance
- tune session behavior for interactive vs headless usage

## Session Operations

| Action | CLI Example | Outcome |
|:-------|:------------|:--------|
| start session | `goose session` | interactive agent loop |
| start named session | `goose session -n release-hardening` | easier recovery/resume |
| web session | `goose web --open` | browser-based interaction |

## Context Management Model

Goose uses two layers:

1. auto-compaction near token thresholds
2. fallback context strategies when limits are still exceeded

Useful environment controls include:

- `GOOSE_AUTO_COMPACT_THRESHOLD`
- `GOOSE_CONTEXT_STRATEGY`
- `GOOSE_MAX_TURNS`

## Practical Tuning

- interactive debugging: use `prompt` strategy for control
- headless flows: use `summarize` for continuity
- high-risk automation: lower max turns and require approvals

## Source References

- [Session Management](https://block.github.io/goose/docs/guides/sessions/session-management)
- [Smart Context Management](https://block.github.io/goose/docs/guides/sessions/smart-context-management)
- [Logs and Session Records](https://block.github.io/goose/docs/guides/logs)

## Summary

You now know how to run longer Goose sessions without uncontrolled context growth.

Next: [Chapter 6: Extensions and MCP Integration](06-extensions-and-mcp-integration.md)
