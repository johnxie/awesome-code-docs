---
layout: default
title: "Chapter 5: Keyboard Shortcuts"
nav_order: 5
has_children: false
parent: "Obsidian Outliner Plugin"
---

# Chapter 5: Keyboard Shortcuts

This chapter explains command registration and hotkey handling for outliner workflows.

## Command Registration Model

- register named commands with explicit editor preconditions
- map commands to default hotkeys and user overrides
- keep command handlers deterministic and side-effect bounded

## Shortcut Priorities

1. editor-native shortcut handling
2. plugin command interception
3. fallback to Obsidian default behavior

## Reliability Practices

- avoid conflicting defaults with common Obsidian shortcuts
- provide discoverable command palette names
- ensure all shortcuts work with nested list contexts

## Summary

You now understand how the plugin wires keyboard-first editing into Obsidian's command system.

Next: [Chapter 6: Testing and Debugging](06-testing-debugging.md)
