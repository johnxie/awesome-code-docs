---
layout: default
title: "Chapter 3: Clients and Runtime Compatibility"
nav_order: 3
parent: Awesome MCP Servers Tutorial
---

# Chapter 3: Clients and Runtime Compatibility

This chapter maps server choices to host client constraints, transport assumptions, and runtime boundaries.

## Learning Goals

- avoid client/server compatibility mismatches before install
- choose local versus remote server patterns intentionally
- account for credential, filesystem, and network access boundaries
- design smaller compatibility pilots before production rollout

## Compatibility Checklist

| Layer | Validation Question |
|:------|:--------------------|
| Host client | Which MCP host will call this server in production? |
| Transport/runtime | Does the server require local process access, HTTP endpoints, or both? |
| Credentials | How are secrets managed and rotated for this server? |
| Data boundaries | What local files, APIs, or services become reachable? |

## Integration Pattern

- start from client capabilities and trust boundaries
- select server candidates that minimize privilege surface
- test with restricted credentials and a narrow task scope
- expand only after execution quality and safety checks pass

## Source References

- [README Clients Section](https://github.com/punkpeye/awesome-mcp-servers/blob/main/README.md#clients)
- [Awesome MCP Clients](https://github.com/punkpeye/awesome-mcp-clients)

## Summary

You now have a compatibility-first approach that reduces runtime surprises and unsafe defaults.

Next: [Chapter 4: Server Selection and Quality Rubric](04-server-selection-and-quality-rubric.md)
