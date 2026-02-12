---
layout: default
title: "Chapter 4: Authentication and Provider Routing"
nav_order: 4
parent: Kilo Code Tutorial
---

# Chapter 4: Authentication and Provider Routing

Authentication and provider selection govern model access, usage limits, and runtime behavior.

## Key Flows

- browser-based login callback flow
- token persistence for future sessions
- provider/api-key routing through settings and environment

## Source References

- [Auth login command implementation](https://github.com/Kilo-Org/kilocode/blob/main/apps/cli/src/commands/auth/login.ts)
- [CLI run command provider setup](https://github.com/Kilo-Org/kilocode/blob/main/apps/cli/src/commands/cli/run.ts)

## Summary

You now understand how Kilo handles auth and provider initialization end-to-end.

Next: [Chapter 5: Session, History, and Context Persistence](05-session-history-and-context-persistence.md)
