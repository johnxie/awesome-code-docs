---
layout: default
title: "Chapter 4: Docker Web Mode and CLI Operations"
nav_order: 4
parent: AgenticSeek Tutorial
---

# Chapter 4: Docker Web Mode and CLI Operations

This chapter compares the two primary execution surfaces and shows how to operate each reliably.

## Learning Goals

- choose web mode or CLI mode based on workload
- run service startup paths correctly for each mode
- understand `SEARXNG_BASE_URL` differences between host and Docker contexts
- verify startup readiness before issuing expensive tasks

## Web Mode (Default)

Use this when you want browser-based interaction and full Docker orchestration.

```bash
./start_services.sh full
```

Expected behavior:

- backend + frontend + searxng + redis start together
- UI available at `http://localhost:3000`
- first startup may take several minutes

## CLI Mode

Use this when you need terminal-native execution and host-installed dependencies.

```bash
./install.sh
./start_services.sh
uv run python -m ensurepip
uv run cli.py
```

CLI mode requires host-aware values like:

- `SEARXNG_BASE_URL="http://localhost:8080"`

## Mode Selection Heuristics

- use web mode for team demos and visual monitoring
- use CLI mode for terminal automation and fast iteration
- use explicit prompts in both modes to improve routing reliability

## Source References

- [README Start Services and Run](https://github.com/Fosowl/agenticSeek/blob/main/README.md#start-services-and-run)
- [CLI Entrypoint](https://github.com/Fosowl/agenticSeek/blob/main/cli.py)
- [Windows Startup Script](https://github.com/Fosowl/agenticSeek/blob/main/start_services.cmd)

## Summary

You now know how to operate both web and CLI execution modes safely.

Next: [Chapter 5: Tools, Browser Automation, and Workspace Governance](05-tools-browser-automation-and-workspace-governance.md)
