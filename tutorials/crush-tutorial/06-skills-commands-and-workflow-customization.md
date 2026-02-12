---
layout: default
title: "Chapter 6: Skills, Commands, and Workflow Customization"
nav_order: 6
parent: Crush Tutorial
---

# Chapter 6: Skills, Commands, and Workflow Customization

This chapter turns Crush into a reusable engineering system rather than a one-off assistant.

## Learning Goals

- use Agent Skills in local and project scopes
- load custom markdown commands from supported directories
- integrate MCP prompts into command workflows
- standardize reusable patterns across teams

## Skills Discovery Paths

Crush can discover skills from:

- `~/.config/crush/skills` (Unix)
- `%LOCALAPPDATA%\crush\skills` (Windows)
- additional paths in `options.skills_paths`

## Custom Command Sources

From internal command loading behavior, custom commands are read from:

- XDG config command dir
- `~/.crush/commands`
- project command directory under configured data path

This supports personal command libraries plus project-scoped commands.

## Workflow Pattern

1. encode standards in `SKILL.md` packages
2. add repeatable command snippets for frequent tasks
3. keep project-specific commands near repository workflows
4. review command/tool permissions with every rollout

## Source References

- [Crush README: Agent Skills](https://github.com/charmbracelet/crush/blob/main/README.md#agent-skills)
- [Crush README: Initialization](https://github.com/charmbracelet/crush/blob/main/README.md#initialization)
- [Command loader source](https://github.com/charmbracelet/crush/blob/main/internal/commands/commands.go)

## Summary

You now have the building blocks for durable, reusable Crush workflows.

Next: [Chapter 7: Logs, Debugging, and Operations](07-logs-debugging-and-operations.md)
