---
layout: default
title: "Chapter 2: Architecture Overview"
nav_order: 2
parent: Bolt.diy Tutorial
---

# Chapter 2: Architecture Overview

bolt.diy combines a chat-driven AI orchestration layer with an interactive code workspace.

## Core Stack

- frontend/runtime: Remix + React + Vite
- package/tooling: pnpm-based monorepo-style workflows
- optional desktop distribution: Electron
- deployment targets: browser-hosted and desktop-native

## High-Level Flow

1. user submits prompt
2. model provider is selected/routed
3. generated plan/code operations are emitted
4. workspace files are updated with diff visibility
5. user reviews, iterates, and runs commands

## Subsystems

| Subsystem | Responsibility |
|:----------|:---------------|
| Chat/Prompt Engine | prompt management and response streaming |
| Workspace Manager | file tree, mutations, and snapshots |
| Terminal Integration | command execution and output display |
| Provider Config Layer | API keys, endpoints, model lists |
| Deploy/Export Layer | packaging and deployment workflows |

## Architecture Tradeoffs

- browser-first UX vs strict enterprise controls
- rapid generation loops vs deterministic change governance
- broad provider support vs configuration complexity

## Summary

You now understand where prompt orchestration, file edits, and runtime execution are coordinated.

Next: [Chapter 3: Providers and Model Routing](03-providers-and-routing.md)
