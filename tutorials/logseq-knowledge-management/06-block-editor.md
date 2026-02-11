---
layout: default
title: "Chapter 6: Block Editor"
nav_order: 6
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 6: Block Editor

The block editor is where text editing, structural hierarchy, and graph references converge.

## Core Interaction Model

- indentation/outdent controls hierarchy
- inline references create graph edges
- keyboard-first commands optimize authoring speed
- slash commands trigger structured actions/templates

## Engineering Challenges

| Challenge | Why It Is Hard |
|:----------|:---------------|
| nested selection behavior | text + structure edits overlap |
| undo/redo correctness | must restore both text and tree shape |
| low-latency updates | large pages can trigger heavy recalculation |
| IME/multilingual editing | composition events complicate key handling |

## Reliability Patterns

- incremental state updates for large documents
- deterministic edit transactions
- robust cursor restoration after structural edits
- regression tests for keyboard workflows

## UX Quality Signals

- predictable tab/shift-tab behavior
- no cursor jumps during auto-formatting
- stable performance in deeply nested pages

## Summary

You can now analyze editor behavior as transaction-safe graph and text mutations.

Next: [Chapter 7: Bi-Directional Links](07-bidirectional-links.md)
