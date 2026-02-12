---
layout: default
title: "Chapter 3: Tooling and Approval Workflow"
nav_order: 3
parent: Mistral Vibe Tutorial
---

# Chapter 3: Tooling and Approval Workflow

Vibe uses a tool-driven workflow for file operations, search, shell execution, and user interaction.

## Core Tool Classes

| Tool Class | Example Capabilities |
|:-----------|:---------------------|
| file tools | read/write/patch files |
| shell tools | command execution in terminal context |
| search tools | grep and project search |
| coordination tools | todo tracking and user questions |

## Approval Model

Default interactive mode is approval-aware, while auto-approve settings should be constrained to trusted contexts.

## Source References

- [Mistral Vibe README: toolset overview](https://github.com/mistralai/mistral-vibe/blob/main/README.md)

## Summary

You now understand how Vibe turns prompts into controlled tool execution loops.

Next: [Chapter 4: Skills and Slash Command Extensions](04-skills-and-slash-command-extensions.md)
