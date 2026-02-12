---
layout: default
title: "Chapter 4: Configuration, Modes, and Context Injection"
nav_order: 4
parent: Claude-Mem Tutorial
---

# Chapter 4: Configuration, Modes, and Context Injection

This chapter covers the highest-leverage controls for memory quality and context relevance.

## Learning Goals

- tune core settings in `~/.claude-mem/settings.json`
- configure model/provider options and runtime defaults
- control context injection filters and display behavior
- avoid over-injection and noisy memory surfaces

## Key Configuration Areas

- model/provider selection
- worker and data directory settings
- context injection filtering and presentation
- mode and behavior toggles for memory retrieval

## Configuration Hygiene

- track settings changes in small increments
- validate one config change per session when debugging
- keep project-level context expectations documented

## Source References

- [Configuration Guide](https://docs.claude-mem.ai/configuration)
- [Folder Context Files](https://docs.claude-mem.ai/usage/folder-context)
- [README Configuration](https://github.com/thedotmack/claude-mem/blob/main/README.md#configuration)

## Summary

You now know how to tune Claude-Mem behavior for accurate, low-noise context injection.

Next: [Chapter 5: Search Tools and Progressive Disclosure](05-search-tools-and-progressive-disclosure.md)
