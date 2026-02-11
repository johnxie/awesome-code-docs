---
layout: default
title: "Chapter 8: Rich Text"
nav_order: 8
has_children: false
parent: "Athens Research Knowledge Graph"
---

# Chapter 8: Rich Text

This chapter covers rich-text parsing and rendering tradeoffs in a block-based graph system.

## Parsing Concerns

- Preserve plain-text round trips.
- Support markdown-like formatting predictably.
- Keep references and embeds as typed tokens.

## Rendering Pipeline

1. Parse source text into tokens.
2. Convert tokens to normalized AST.
3. Render AST to Reagent components.
4. Map edits back to block text safely.

## Production Guardrails

- Reject malformed token trees early.
- Limit untrusted embed/render operations.
- Add snapshot tests for parser regressions.

## Final Summary

You now have complete Athens core coverage from architecture through editor and rich text internals.

Related:
- [Athens Index](../index.md)
- [Setup Guide](setup.md)
