---
layout: default
title: "Chapter 8: Production Operations"
nav_order: 8
parent: HAPI Tutorial
---

# Chapter 8: Production Operations

This chapter closes with reliability and scaling patterns for team and organizational HAPI usage.

## Operational Baseline

- monitor hub availability and event-stream health
- track session counts, approval latency, and error classes
- back up and maintain SQLite state lifecycle
- define incident paths for relay/tunnel/provider failures

## Scaling Signals

| Signal | Why It Matters |
|:-------|:---------------|
| active session concurrency | capacity planning |
| message and approval lag | UX and operational risk |
| failed remote actions | networking/auth reliability |
| reconnect frequency | tunnel/transport stability |

## Runbook Priorities

1. restore connectivity and auth first
2. preserve session state integrity
3. communicate user-facing impact windows
4. review root cause and tighten controls

## Final Summary

You now have end-to-end guidance for running HAPI from single-user local workflows to production-ready remote control operations.

Related:
- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
