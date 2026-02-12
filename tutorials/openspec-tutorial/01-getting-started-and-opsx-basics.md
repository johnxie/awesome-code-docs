---
layout: default
title: "Chapter 1: Getting Started and OPSX Basics"
nav_order: 1
parent: OpenSpec Tutorial
---

# Chapter 1: Getting Started and OPSX Basics

This chapter establishes a reliable OpenSpec baseline and clarifies the core OPSX command model.

## Learning Goals

- install OpenSpec with supported package managers
- initialize a project and generate workflow assets
- run first OPSX commands with clean expectations

## Prerequisites

| Requirement | Why It Matters |
|:------------|:---------------|
| Node.js 20.19.0+ | minimum runtime requirement |
| an AI coding assistant client | OPSX commands are consumed through tool integrations |
| writable project directory | OpenSpec generates artifact and skill files |

## Install and Initialize

```bash
npm install -g @fission-ai/openspec@latest
cd your-project
openspec init
```

`openspec init` creates an `openspec/` directory and configures selected tool integrations.

## First Workflow Loop

1. `/opsx:new <change-name>`
2. `/opsx:ff` or `/opsx:continue`
3. `/opsx:apply`
4. `/opsx:archive`

## Baseline Validation

| Check | Command |
|:------|:--------|
| version installed | `openspec --version` |
| current change status | `openspec status` |
| generated structure | inspect `openspec/specs` and `openspec/changes` |

## Source References

- [README Quick Start](https://github.com/Fission-AI/OpenSpec/blob/main/README.md)
- [Installation Guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md)
- [Getting Started Guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)

## Summary

You now have a working OpenSpec environment with the core workflow entry points.

Next: [Chapter 2: Artifact Graph and Change Lifecycle](02-artifact-graph-and-change-lifecycle.md)
