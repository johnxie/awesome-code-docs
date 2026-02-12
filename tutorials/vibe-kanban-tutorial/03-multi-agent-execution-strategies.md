---
layout: default
title: "Chapter 3: Multi-Agent Execution Strategies"
nav_order: 3
parent: Vibe Kanban Tutorial
---

# Chapter 3: Multi-Agent Execution Strategies

This chapter focuses on execution patterns that maximize throughput while protecting quality.

## Learning Goals

- choose between parallel and sequential execution modes
- assign tasks by risk and dependency profile
- reduce collisions across agent workstreams
- prevent low-value churn in large agent batches

## Strategy Matrix

| Strategy | Best For | Risk |
|:---------|:---------|:-----|
| parallel tasks | independent tickets and broad exploration | review overhead if poorly scoped |
| sequential pipeline | dependent tasks and staged refactors | slower throughput |
| hybrid mode | mixed backlogs with shared constraints | requires stronger orchestration discipline |

## Practical Rules

1. parallelize only tasks with clear dependency boundaries
2. run critical architectural tasks sequentially with checkpoints
3. reserve human review gates for destructive or high-impact changes

## Source References

- [Vibe Kanban README: parallel/sequential orchestration](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#overview)
- [Vibe Kanban Docs](https://vibekanban.com/docs)

## Summary

You now can structure multi-agent execution for both speed and reliability.

Next: [Chapter 4: MCP and Configuration Control](04-mcp-and-configuration-control.md)
