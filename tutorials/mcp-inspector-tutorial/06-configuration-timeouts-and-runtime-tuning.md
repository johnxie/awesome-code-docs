---
layout: default
title: "Chapter 6: Configuration, Timeouts, and Runtime Tuning"
nav_order: 6
parent: MCP Inspector Tutorial
---

# Chapter 6: Configuration, Timeouts, and Runtime Tuning

The default timeout behavior is good for quick tests, but long-running tools and interactive flows need explicit tuning.

## Learning Goals

- tune request timeout values for realistic workloads
- use progress-aware timeout reset behavior correctly
- separate client-side timeout policy from server-side limits
- manage profile-like configs for multiple targets

## Key Runtime Settings

| Setting | Purpose | Typical Adjustment |
|:--------|:--------|:-------------------|
| `MCP_SERVER_REQUEST_TIMEOUT` | client request timeout | increase for slow tool operations |
| `MCP_REQUEST_TIMEOUT_RESET_ON_PROGRESS` | extend timeout on progress events | keep enabled for streaming/progress tools |
| `MCP_REQUEST_MAX_TOTAL_TIMEOUT` | max total duration cap | set upper bound for long tasks |
| `MCP_PROXY_FULL_ADDRESS` | non-default proxy address | required for remote/devbox scenarios |
| `MCP_AUTO_OPEN_ENABLED` | browser auto-open behavior | disable in CI/headless contexts |

## Practical Rule

Set Inspector timeout ceilings high enough for legitimate long calls, but keep a finite max timeout to prevent invisible hangs.

## Source References

- [Inspector README - Configuration](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#configuration)
- [Inspector README - Note on Timeouts](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#configuration)

## Summary

You now have a runtime tuning approach that reduces false failures and stalled sessions.

Next: [Chapter 7: Inspector in Server Development Lifecycle](07-inspector-in-server-development-lifecycle.md)
