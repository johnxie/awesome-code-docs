---
layout: default
title: "Chapter 8: Production Operations"
nav_order: 8
parent: HAPI Tutorial
---

# Chapter 8: Production Operations

This chapter closes with production reliability patterns for HAPI hub operations.

## Operational Baseline

- monitor hub uptime and API/SSE health
- track session concurrency and approval latency
- back up and validate SQLite persistence lifecycle
- maintain runbooks for relay/tunnel/auth failures

## Key Metrics

| Metric | Operational Value |
|:-------|:------------------|
| active sessions | capacity planning |
| mean approval latency | responsiveness and risk signal |
| failed action relay count | transport/auth quality |
| reconnect frequency | network stability insight |

## Incident Response Priorities

1. restore authenticated connectivity
2. protect session state integrity
3. communicate impact and expected recovery time
4. perform root-cause review and tighten controls

## Final Summary

You now have an operational model for running HAPI at production scale with controlled remote agent workflows.

Related:
- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
