---
layout: default
title: "Chapter 7: Runtime Coverage: Browser, Node, Deno, and Edge"
nav_order: 7
parent: Fireproof Tutorial
---

# Chapter 7: Runtime Coverage: Browser, Node, Deno, and Edge

Fireproof is designed for broad JavaScript runtime portability with one API shape.

## Runtime Strategy

| Runtime | Notes |
|:--------|:------|
| Browser | first-class local-first target |
| Node.js | core API and file-based persistence |
| Deno | supported with runtime flags and config |
| Edge/cloud contexts | used through gateway/protocol adapters |

## Adoption Guidance

- pick one canonical runtime for baseline tests
- validate gateway behavior in each target environment
- avoid runtime-specific assumptions in shared domain logic

## Source References

- [Fireproof README: runtime support](https://github.com/fireproof-storage/fireproof/blob/main/README.md)
- [Monorepo runtime modules](https://github.com/fireproof-storage/fireproof/tree/main/core/runtime)

## Summary

You now have a portability model for deploying Fireproof across browser and server contexts.

Next: [Chapter 8: Production Operations, Security, and Debugging](08-production-operations-security-and-debugging.md)
