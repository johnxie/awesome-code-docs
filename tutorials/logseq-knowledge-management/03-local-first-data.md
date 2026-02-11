---
layout: default
title: "Chapter 3: Local-First Data"
nav_order: 3
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 3: Local-First Data

Logseq's local-first model centers on user-owned files with graph indexing layered on top.

## Storage Principles

- markdown/org files are canonical source of truth
- index/cache layers accelerate queries and backlinks
- core workflows remain usable offline

## Consistency Model

In practice, systems must reconcile:

1. file-system truth
2. in-memory graph state
3. rendered UI state

Robust implementations include deterministic reload/index rebuild paths when state diverges.

## Durability and Recovery

- atomic file writes where possible
- deterministic block IDs for stable references
- index rebuild tools for corruption scenarios
- clear conflict resolution strategy for sync setups

## Local-First Benefits

- data portability and longevity
- lower dependence on hosted services
- predictable offline behavior

## Summary

You can now evaluate local-first tradeoffs and design recovery pathways that protect data integrity.

Next: [Chapter 4: Development Setup](04-development-setup.md)
