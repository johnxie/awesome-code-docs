---
layout: default
title: "Chapter 5: Refly CLI and Claude Code Skill Export"
nav_order: 5
parent: Refly Tutorial
---

# Chapter 5: Refly CLI and Claude Code Skill Export

This chapter explains how to use the CLI for deterministic workflow operations and how Refly skills connect to Claude Code contexts.

## Learning Goals

- run builder/validation/commit loops from terminal
- use structured CLI output for automation chains
- export/install skills for Claude Code-oriented workflows
- keep orchestration reproducible across environments

## High-Value CLI Flow

```bash
npm install -g @refly/cli
refly init
refly login
refly builder start --name "my-workflow"
refly builder validate
refly builder commit
refly workflow run <workflowId>
```

## Claude Code-Oriented Skill Path

- `refly init` installs skill references into Claude directories
- skill operations can be managed with `refly skill ...` commands
- exported skills can be used in Claude Code and other MCP-capable contexts

## Source References

- [Refly CLI README](https://github.com/refly-ai/refly/blob/main/packages/cli/README.md)
- [CLI Skill Reference](https://github.com/refly-ai/refly/blob/main/packages/cli/skill/SKILL.md)
- [README: Skills for Claude Code](https://github.com/refly-ai/refly/blob/main/README.md#use-case-3-skills-for-claude-code)

## Summary

You now have a deterministic CLI path for building, validating, and exporting workflow capabilities.

Next: [Chapter 6: Observability, Deployment, and Operations](06-observability-deployment-and-operations.md)
