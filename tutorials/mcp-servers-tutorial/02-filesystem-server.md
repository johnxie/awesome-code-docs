---
layout: default
title: "Chapter 2: Filesystem Server"
nav_order: 2
parent: MCP Servers Tutorial
---

# Chapter 2: Filesystem Server

Filesystem servers are a core MCP pattern for safe file access and editing.

## Core Capabilities

- List directories
- Read/write files
- Search text in files
- Resolve paths safely

## Safety Pattern

- Restrict operations to allowed roots.
- Normalize and validate paths.
- Block traversal attempts (`../`).

## Example Guardrail Pseudocode

```python
def resolve_safe(root: str, requested: str) -> str:
    resolved = realpath(join(root, requested))
    if not resolved.startswith(realpath(root) + "/"):
        raise ValueError("Path escapes allowed root")
    return resolved
```

## Summary

You can now reason about secure filesystem operations in MCP servers.

Next: [Chapter 3: Git Server](03-git-server.md)
