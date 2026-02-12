---
layout: default
title: "Chapter 4: Language Backends and Analysis Strategy"
nav_order: 4
parent: Serena Tutorial
---

# Chapter 4: Language Backends and Analysis Strategy

This chapter covers the backend choices that determine semantic quality and operational complexity.

## Learning Goals

- understand Serena's backend options
- choose between LSP and JetBrains-plugin pathways
- align backend choice with project language coverage
- avoid backend-related reliability pitfalls

## Backend Options

| Backend | Strengths | Tradeoffs |
|:--------|:----------|:----------|
| LSP-based analysis | open, broad language support | depends on per-language server setup |
| Serena JetBrains plugin | deep IDE-native analysis | requires JetBrains IDE environment |

Serena reports support for 30+ languages through its LSP abstraction.

## Selection Guidance

- choose LSP for cross-editor, infrastructure-friendly setups
- choose JetBrains plugin for strongest IDE-assisted semantics
- document required backend dependencies per language stack

## Source References

- [Language Support](https://oraios.github.io/serena/01-about/020_programming-languages.html)
- [Serena JetBrains Plugin](https://oraios.github.io/serena/02-usage/025_jetbrains_plugin.html)

## Summary

You now can select analysis backend strategy based on workflow, language set, and team environment.

Next: [Chapter 5: Project Workflow and Context Practices](05-project-workflow-and-context-practices.md)
