---
layout: default
title: "Chapter 2: Agent Profiles and Trust Model"
nav_order: 2
parent: Mistral Vibe Tutorial
---

# Chapter 2: Agent Profiles and Trust Model

Vibe provides multiple built-in agent profiles and a trust-folder mechanism to reduce accidental unsafe execution.

## Built-In Agent Profiles

| Agent | Intended Use |
|:------|:-------------|
| `default` | standard prompts with approval checks |
| `plan` | read-focused planning/exploration |
| `accept-edits` | auto-approve edit tools only |
| `auto-approve` | broad automation mode, highest risk |

## Trust Folder Behavior

Vibe maintains trusted-folder state to prevent unintentional execution in unknown directories.

## Source References

- [Mistral Vibe README: built-in agents](https://github.com/mistralai/mistral-vibe/blob/main/README.md)
- [Mistral Vibe README: trust folder system](https://github.com/mistralai/mistral-vibe/blob/main/README.md)

## Summary

You now understand how to pick agent profiles and use trust controls safely.

Next: [Chapter 3: Tooling and Approval Workflow](03-tooling-and-approval-workflow.md)
