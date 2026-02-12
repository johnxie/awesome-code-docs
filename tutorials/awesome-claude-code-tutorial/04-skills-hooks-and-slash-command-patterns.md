---
layout: default
title: "Chapter 4: Skills, Hooks, and Slash Command Patterns"
nav_order: 4
parent: Awesome Claude Code Tutorial
---

# Chapter 4: Skills, Hooks, and Slash Command Patterns

This chapter extracts reusable operating patterns from the most practical resource categories.

## Learning Goals

- distinguish when to use skills, hooks, and slash commands
- compose these resource types into one coherent workflow
- avoid over-automation before baseline reliability exists
- create a phased rollout strategy for your project

## Capability Layering

| Resource Type | Primary Role | Good First Use |
|:--------------|:-------------|:---------------|
| skills | domain-specific execution capability | repetitive coding/review tasks |
| hooks | lifecycle enforcement and guardrails | formatting, test checks, notifications |
| slash commands | structured task entrypoints | routine planning, review, deploy flows |

## Rollout Strategy

1. start with one high-value slash command
2. add one hook for quality guardrails
3. introduce skills for specialized workflows
4. measure whether each new layer lowers error rate or cycle time

## Source References

- [Skills Resources](https://github.com/hesreallyhim/awesome-claude-code/tree/main/resources)
- [Slash Commands Resources](https://github.com/hesreallyhim/awesome-claude-code/tree/main/resources/slash-commands)
- [Hooks Resources](https://github.com/hesreallyhim/awesome-claude-code/tree/main/resources)

## Summary

You now have a practical model for composing multiple resource types without adding chaos.

Next: [Chapter 5: `CLAUDE.md` and Project Scaffolding Patterns](05-claude-md-and-project-scaffolding-patterns.md)
