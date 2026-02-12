---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Shotgun Tutorial
---

# Chapter 1: Getting Started

This chapter gets Shotgun running in a repository so you can generate your first spec-driven workflow.

## Quick Start

```bash
uvx shotgun-sh@latest
```

## Recommended First Session

1. Launch Shotgun in your project directory.
2. Let it index the repository when prompted.
3. Start with a research-oriented request before asking for implementation.

Example prompt:

```text
Research how authentication currently works and propose a staged implementation plan for password reset.
```

## Core Setup Notes

- Python: 3.11+
- install method: `uvx shotgun-sh@latest`
- default interaction: TUI-first workflow
- default execution mode: Planning

## Source References

- [Shotgun README](https://github.com/shotgun-sh/shotgun)
- [Installation section](https://github.com/shotgun-sh/shotgun#-installation)

## Summary

You now have Shotgun running with a first research and planning loop.

Next: [Chapter 2: Router Architecture and Agent Lifecycle](02-router-architecture-and-agent-lifecycle.md)
