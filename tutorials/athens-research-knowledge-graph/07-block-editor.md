---
layout: default
title: "Chapter 7: Block Editor"
nav_order: 7
has_children: false
parent: "Athens Research Knowledge Graph"
---

# Chapter 7: Block Editor

The block editor is the center of Athens' UX and data model.

## Core Editor Behaviors

- Enter creates sibling blocks.
- Tab/Shift-Tab changes hierarchy depth.
- Backspace at start merges or lifts blocks.
- `[[...]]` creates structured references.

## Editor State Model

Track editor state separately from persisted graph state:

- cursor/selection range
- composition state (IME, pending transforms)
- active command palette context

## Command Handling Pattern

```text
key input -> editor command -> local state update -> persistence effect
```

## Quality Checklist

- Cursor behavior is deterministic across nested blocks.
- Undo/redo spans structural edits, not only text deltas.
- Reference creation preserves block UUID identity.

## Summary

You can now reason about Athens editor behavior and command pipelines.

Next: [Chapter 8: Rich Text](08-rich-text.md)
