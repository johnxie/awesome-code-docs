---
layout: default
title: "Chapter 4: Agents, Skills, and Command Orchestration"
nav_order: 4
parent: Everything Claude Code Tutorial
---

# Chapter 4: Agents, Skills, and Command Orchestration

This chapter focuses on day-to-day orchestration patterns.

## Learning Goals

- route tasks through commands with minimal ambiguity
- choose the right specialist agent for each task class
- activate supporting skills for quality and speed
- structure complex workflows into deterministic phases

## Orchestration Pattern

- `plan` before execution
- delegate to specialized agents during implementation
- run review/security passes before merge
- close with verification and learnings capture

## Suggested Command Chain

`/plan` -> `/tdd` -> `/code-review` -> `/verify` -> `/learn`

## Source References

- [Commands Directory](https://github.com/affaan-m/everything-claude-code/tree/main/commands)
- [Agents Directory](https://github.com/affaan-m/everything-claude-code/tree/main/agents)
- [Skills Directory](https://github.com/affaan-m/everything-claude-code/tree/main/skills)

## Summary

You now have a practical command/agent orchestration baseline.

Next: [Chapter 5: Hooks, MCP, and Continuous Learning Loops](05-hooks-mcp-and-continuous-learning-loops.md)
