---
layout: default
title: "Chapter 3: Local-First Data"
nav_order: 3
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 3: Local-First Data

Logseq's local-first model combines plain-text files with indexed graph state.

## Storage Principles

- Markdown/Org files remain user-owned source of truth.
- Datascript index accelerates query and traversal.
- Sync is optional, not required for core app behavior.

## Integrity Practices

- Use deterministic block IDs.
- Rebuild index from files on corruption recovery.
- Keep file writes atomic for crash safety.

## Summary

You can now reason about Logseq's local durability and synchronization tradeoffs.

Next: [Chapter 4: Development Setup](04-development-setup.md)
