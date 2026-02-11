---
layout: default
title: "Chapter 5: Block Data Model"
nav_order: 5
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 5: Block Data Model

Blocks are Logseq's atomic knowledge units.

## Block Fields

- stable UUID
- text/content payload
- parent-child hierarchy
- page and backlink relationships
- metadata (timestamps, properties, tags)

## Model Constraints

- parent references must remain acyclic
- order indexes must be deterministic
- link refs must survive text edits

## Summary

You can now map user edits to the underlying block graph model.

Next: [Chapter 6: Block Editor](06-block-editor.md)
