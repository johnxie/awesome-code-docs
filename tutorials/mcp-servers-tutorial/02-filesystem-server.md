---
layout: default
title: "Chapter 2: Filesystem Server"
nav_order: 2
parent: MCP Servers Tutorial
---

# Chapter 2: Filesystem Server

The filesystem server is the canonical example of capability scoping and safe tool design.

## What It Provides

The official filesystem server exposes tools for:

- reading text and media files
- writing/editing/moving files
- listing/searching directories
- querying file metadata
- enumerating currently allowed directories

## Access Control Model

The key design is **allowlisted directory boundaries**.

Two configuration methods are supported:

1. command-line allowed roots
2. dynamic roots from clients that support the MCP roots protocol

When roots are provided by the client, they replace static startup roots.

## Why Roots Matter

Dynamic roots allow clients to adjust accessible scope at runtime without restarting the server. This is convenient, but it increases the need for:

- explicit trust boundaries
- event logging for root changes
- policy checks before privileged operations

## Tool Annotation Pattern

The server marks tools with hints (read-only, idempotent, destructive). These hints are valuable for client UX and safety policies.

Example policy usage:

- auto-run read-only tools
- require confirmation for destructive tools
- require stronger policy checks on non-idempotent mutations

## Safe Edit Pattern

Use dry-run where available before mutating files.

```text
1) run edit in preview mode
2) inspect diff
3) apply if expected
```

This mirrors modern CI-safe change workflows and reduces accidental corruption.

## Threats to Address in Production

- path traversal and symlink edge cases
- unexpected binary payload handling
- overly broad root configuration
- insufficient audit metadata for writes

## Summary

You now understand the filesystem server's core safety model and how to adapt it responsibly.

Next: [Chapter 3: Git Server](03-git-server.md)
