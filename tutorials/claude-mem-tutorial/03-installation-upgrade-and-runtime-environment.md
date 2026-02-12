---
layout: default
title: "Chapter 3: Installation, Upgrade, and Runtime Environment"
nav_order: 3
parent: Claude-Mem Tutorial
---

# Chapter 3: Installation, Upgrade, and Runtime Environment

This chapter focuses on keeping installation and upgrade workflows repeatable.

## Learning Goals

- run standard and advanced installation paths safely
- verify required runtime dependencies and auto-install behavior
- apply upgrade flow with minimal downtime risk
- understand platform-specific environment differences

## Runtime Dependencies

Claude-Mem relies on a mixed runtime stack, including:

- Node.js runtime baseline
- Bun for worker/service process management
- uv/Python components for vector search pathways
- SQLite for durable storage

## Upgrade Pattern

- snapshot current settings and data directory
- upgrade plugin version/channel deliberately
- verify worker health and context retrieval
- run a small session replay test before full usage

## Platform Notes

- watch Windows PATH/runtime setup carefully
- monitor local port conflicts for viewer/worker services
- keep terminal and shell environment consistent across sessions

## Source References

- [Installation Guide](https://docs.claude-mem.ai/installation)
- [Development Guide](https://docs.claude-mem.ai/development)
- [README System Requirements](https://github.com/thedotmack/claude-mem/blob/main/README.md#system-requirements)

## Summary

You now have a stable install/upgrade pattern for Claude-Mem environments.

Next: [Chapter 4: Configuration, Modes, and Context Injection](04-configuration-modes-and-context-injection.md)
