---
layout: default
title: "Chapter 3: Session Lifecycle and Handoff"
nav_order: 3
parent: HAPI Tutorial
---

# Chapter 3: Session Lifecycle and Handoff

HAPI's defining capability is seamless control handoff between terminal and remote devices.

## Session Lifecycle

1. user starts `hapi` locally
2. CLI registers session with hub
3. hub persists session and broadcasts updates
4. remote client sends messages/approvals
5. CLI continues agent execution without restarting context

## Handoff Model

```mermaid
graph LR
    L[Local Terminal Control] <--> R[Remote Phone/Web Control]
    L --> S[Same Session State]
    R --> S
```

## Operational Benefits

- no context reset while switching devices
- async approvals while away from workstation
- easier long-running task supervision without terminal lock-in

## Summary

You can now design workflows that intentionally switch between local focus and remote supervision.

Next: [Chapter 4: Remote Access and Networking](04-remote-access-and-networking.md)
