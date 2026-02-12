---
layout: default
title: "Chapter 6: AutoYes, Daemon Polling, and Safety Controls"
nav_order: 6
parent: Claude Squad Tutorial
---

# Chapter 6: AutoYes, Daemon Polling, and Safety Controls

AutoYes features can increase throughput but require strict boundaries.

## Safety Considerations

- `--autoyes` is experimental and should be limited to trusted tasks
- polling/daemon controls affect unattended behavior
- enforce stronger review gates before pushing auto-accepted outputs

## Source References

- [Claude Squad CLI flags](https://github.com/smtg-ai/claude-squad/blob/main/README.md)
- [Config fields including AutoYes and daemon interval](https://github.com/smtg-ai/claude-squad/blob/main/config/config.go)

## Summary

You now understand how to apply automation controls without removing governance.

Next: [Chapter 7: Configuration and State Management](07-configuration-and-state-management.md)
