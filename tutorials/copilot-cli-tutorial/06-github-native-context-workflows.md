---
layout: default
title: "Chapter 6: GitHub-Native Context Workflows"
nav_order: 6
parent: GitHub Copilot CLI Tutorial
---

# Chapter 6: GitHub-Native Context Workflows

Copilot CLI is designed to work with GitHub context out of the box, including repository, issue, and pull request awareness.

## Workflow Advantages

- less context-copying between browser and terminal
- better continuity for issue-to-code execution loops
- tighter mapping between generated changes and GitHub artifacts

## Suggested Pattern

1. begin in target repository root
2. prompt with issue/PR context included
3. review proposed edits before execution
4. validate locally and push through normal Git workflow

## Source References

- [Copilot CLI README: GitHub integration](https://github.com/github/copilot-cli/blob/main/README.md)
- [Official documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## Summary

You now understand how Copilot CLI aligns terminal execution with GitHub development flows.

Next: [Chapter 7: Installation and Update Channels](07-installation-and-update-channels.md)
