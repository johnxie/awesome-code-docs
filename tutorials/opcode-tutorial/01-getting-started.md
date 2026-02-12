---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Opcode Tutorial
---

# Chapter 1: Getting Started

This chapter establishes the baseline for using Opcode with Claude Code.

## Learning Goals

- understand prerequisites and install paths
- launch Opcode and discover local Claude Code projects
- validate first session and project workflow
- triage common setup failures

## Prerequisites

- Claude Code CLI installed and available in `PATH`

## First-Run Flow

1. launch Opcode
2. choose Projects or CC Agents entry point
3. confirm `~/.claude` directory detection
4. open a project and inspect sessions

## Common Startup Issues

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| no projects visible | Claude directory not present | verify Claude Code setup and path |
| claude command errors | CLI not in PATH | reinstall and verify `claude --version` |
| build/install friction | missing platform deps | follow platform-specific source build docs |

## Source References

- [Opcode README: Installation](https://github.com/winfunc/opcode/blob/main/README.md#-installation)
- [Opcode README: Getting Started](https://github.com/winfunc/opcode/blob/main/README.md#getting-started)

## Summary

You now have Opcode connected to a working Claude Code environment.

Next: [Chapter 2: Architecture and Platform Stack](02-architecture-and-platform-stack.md)
