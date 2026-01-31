---
layout: default
title: "Logseq Knowledge Management"
nav_order: 40
has_children: true
---

# Logseq: Deep Dive Tutorial

> **Project**: [Logseq](https://github.com/logseq/logseq) — A privacy-first, local-first knowledge management platform with block-based editing and graph visualization.

[![Stars](https://img.shields.io/github/stars/logseq/logseq?style=social)](https://github.com/logseq/logseq)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![ClojureScript](https://img.shields.io/badge/ClojureScript-Electron-purple)](https://github.com/logseq/logseq)

## What Is Logseq?

Logseq is a local-first, privacy-preserving knowledge management platform built with ClojureScript and Electron. It stores notes as plain Markdown/Org-mode files on your filesystem, provides block-based editing with bi-directional linking, and visualizes your knowledge as an interactive graph.

| Feature | Description |
|---------|-------------|
| **Local-First** | Files stored as plain Markdown on your filesystem |
| **Block-Based** | Atomic content units with outliner-style editing |
| **Bi-Directional Links** | Automatic backlinks and page references |
| **Knowledge Graph** | Interactive D3.js visualization of note connections |
| **Plugin System** | JavaScript plugin API with sandboxed execution |
| **Git Sync** | Built-in Git-based synchronization across devices |

## Architecture Overview

```mermaid
graph TB
    subgraph Desktop["Electron App"]
        EDITOR[Block Editor]
        GRAPH[Graph View]
        SEARCH[Full-Text Search]
        PLUGINS[Plugin Runtime]
    end

    subgraph Core["ClojureScript Core"]
        REFRAME[Re-frame State]
        PARSER[Markdown/Org Parser]
        INDEX[Block Index]
    end

    subgraph Storage["Local Storage"]
        FS[File System / Markdown]
        GIT[Git Sync]
        DB[(Datascript)]
    end

    Desktop --> Core
    Core --> Storage
```

## Tutorial Structure

| Chapter | Topic | What You'll Learn |
|---------|-------|-------------------|
| [1. Knowledge Management Principles](docs/01-knowledge-management-principles.md) | Philosophy | Local-first paradigms, block-based thinking |
| [4. Development Setup](docs/04-development-setup.md) | Setup | ClojureScript + Electron development stack |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | ClojureScript |
| **UI Framework** | Reagent (React wrapper) |
| **State** | Re-frame |
| **Database** | Datascript (in-memory) |
| **Desktop** | Electron |
| **Graph Viz** | D3.js |
| **File Format** | Markdown, Org-mode |

---

Ready to begin? Start with [Chapter 1: Knowledge Management Principles](docs/01-knowledge-management-principles.md).

---

*Built with insights from the [Logseq repository](https://github.com/logseq/logseq) and community documentation.*
