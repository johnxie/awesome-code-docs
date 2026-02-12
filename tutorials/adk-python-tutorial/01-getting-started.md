---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: ADK Python Tutorial
---

# Chapter 1: Getting Started

This chapter gets ADK running locally so you can validate the core developer loop quickly.

## Learning Goals

- install ADK in a clean Python environment
- create a minimal agent project structure
- run with ADK CLI and web tools
- avoid first-run setup pitfalls

## Quick Setup Pattern

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-adk
```

Then create a minimal agent module and run:

```bash
adk web path/to/agents_dir
```

## First-Use Checklist

1. confirm Python and environment are healthy
2. install `google-adk` and launch the UI
3. run one user turn through your root agent
4. verify tool calls and events appear as expected

## Source References

- [ADK README: Installation](https://github.com/google/adk-python/blob/main/README.md#-installation)
- [ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/)
- [ADK CLI Documentation](https://google.github.io/adk-docs/)

## Summary

You now have ADK installed and a working baseline invocation flow.

Next: [Chapter 2: Architecture and Runner Lifecycle](02-architecture-and-runner-lifecycle.md)
