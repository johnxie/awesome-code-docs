---
layout: default
title: "Chapter 3: Git Server"
nav_order: 3
parent: MCP Servers Tutorial
---

# Chapter 3: Git Server

Git servers expose repository intelligence to language-model clients.

## Typical Tools

- status and branch inspection
- diff and commit history retrieval
- file blame and change metadata

## Practical Use Cases

- Auto-generate release notes from commit ranges.
- Explain regressions by comparing diffs.
- Assist code review with targeted file context.

## Risk Controls

- Read-only mode for untrusted contexts.
- Command allowlist and argument validation.
- Execution timeouts for expensive history queries.

## Summary

You understand how MCP Git integrations provide controlled repo context.

Next: [Chapter 4: Memory Server](04-memory-server.md)
