---
layout: default
title: "Chapter 5: Tools, Browser Automation, and Workspace Governance"
nav_order: 5
parent: AgenticSeek Tutorial
---

# Chapter 5: Tools, Browser Automation, and Workspace Governance

This chapter focuses on the highest-risk operational zone: autonomous tool execution over browser and files.

## Learning Goals

- understand the project's tool-block execution model
- reduce risk when agents can browse and write files
- structure workspace paths to avoid accidental data access
- enforce practical run-time safeguards

## Tool Block Contract

AgenticSeek tools are invoked by markdown-style code blocks with a tool name and payload.

Examples documented by the project include blocks like:

````text
```web_search
query text
```
````

This contract is parsed and dispatched by tool infrastructure in `sources/tools`.

## Workspace Governance Baseline

- create a dedicated work directory per project or task class
- avoid pointing `WORK_DIR` at sensitive home-level paths
- treat generated files as untrusted until reviewed
- keep backups for any directory where autonomous writes are enabled

## Browser Automation Risk Controls

- keep `headless_browser=True` for deterministic automated runs
- use `stealth_mode` only when needed for compatibility
- review logs for unexpected navigation or form interactions
- avoid high-privilege authenticated sessions while testing

## Source References

- [Contributing Guide: Tools](https://github.com/Fosowl/agenticSeek/blob/main/docs/CONTRIBUTING.md#implementing-and-using-tools)
- [Tools Source Directory](https://github.com/Fosowl/agenticSeek/tree/main/sources/tools)
- [README Known Issues](https://github.com/Fosowl/agenticSeek/blob/main/README.md#known-issues)

## Summary

You now have practical controls for safer tool execution and browser automation.

Next: [Chapter 6: Model Strategy and Remote Server Mode](06-model-strategy-and-remote-server-mode.md)
