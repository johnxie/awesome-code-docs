---
layout: default
title: "Chapter 6: Tool Integrations and Multi-Agent Portability"
nav_order: 6
parent: OpenSpec Tutorial
---

# Chapter 6: Tool Integrations and Multi-Agent Portability

A major OpenSpec strength is tool portability: one workflow, many coding assistants.

## Learning Goals

- understand how OpenSpec maps skills/commands across tools
- choose integration targets for your team environment
- minimize tool-specific lock-in

## Integration Model

| Layer | Description |
|:------|:------------|
| skills | reusable instruction assets powering OPSX behavior |
| command bindings | tool-specific slash command wiring |
| project artifacts | shared `openspec/` state independent of assistant choice |

## Examples of Supported Ecosystem Paths

- Claude Code
- Cursor
- Continue
- Codex
- OpenCode
- GitHub Copilot
- Windsurf
- RooCode

## Portability Checklist

1. keep workflow semantics in artifacts, not chat history
2. commit OpenSpec directories to version control
3. document tool-specific command paths for onboarding
4. periodically test at least one secondary tool integration

## Source References

- [Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)
- [Commands Reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [README](https://github.com/Fission-AI/OpenSpec/blob/main/README.md)

## Summary

You now understand how OpenSpec reduces migration friction across coding-agent clients.

Next: [Chapter 7: Validation, Automation, and CI Operations](07-validation-automation-and-ci-operations.md)
