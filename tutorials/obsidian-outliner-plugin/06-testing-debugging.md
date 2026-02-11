---
layout: default
title: "Chapter 6: Testing and Debugging"
nav_order: 6
has_children: false
parent: "Obsidian Outliner Plugin"
---

# Chapter 6: Testing and Debugging

Testing outliner behavior requires strong coverage of tree mutations and cursor state.

## High-Value Test Areas

- indent/outdent transformations
- move up/down across nested siblings
- fold/unfold state persistence
- multi-cursor and selection edge cases

## Debugging Workflow

- instrument command entry/exit with structured logs
- snapshot document tree before and after commands
- isolate parser bugs with minimal markdown fixtures

## Summary

You can now design a practical test strategy for editor-heavy plugin behavior.

Next: [Chapter 7: Plugin Packaging](07-plugin-packaging.md)
