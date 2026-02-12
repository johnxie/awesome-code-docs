---
layout: default
title: "Chapter 2: Core Philosophy and the 3-File Pattern"
nav_order: 2
parent: Planning with Files Tutorial
---

# Chapter 2: Core Philosophy and the 3-File Pattern

This chapter explains why durable file memory improves agent execution quality.

## Learning Goals

- understand volatile-context limitations in long tasks
- apply the 3-file model with clear ownership
- use markdown files as working memory, not just output logs
- avoid context stuffing and goal drift

## The 3-File Pattern

- `task_plan.md`: phases, checkpoints, and completion criteria
- `findings.md`: research results and key discoveries
- `progress.md`: chronological execution log and outcomes

## Core Principle

Treat context as RAM and files as disk: anything important must be persisted.

## Source References

- [README The Solution: 3-File Pattern](https://github.com/OthmanAdi/planning-with-files/blob/master/README.md#the-solution-3-file-pattern)
- [Workflow Guide](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/workflow.md)
- [SKILL.md Core Pattern](https://github.com/OthmanAdi/planning-with-files/blob/master/skills/planning-with-files/SKILL.md)

## Summary

You now understand the planning model that keeps long-running tasks stable.

Next: [Chapter 3: Installation Paths Across IDEs and Agents](03-installation-paths-across-ides-and-agents.md)
