---
layout: default
title: "Chapter 2: Core Architecture and Minimal Design"
nav_order: 2
parent: Mini-SWE-Agent Tutorial
---

# Chapter 2: Core Architecture and Minimal Design

This chapter explains the small-core philosophy and its implications.

## Learning Goals

- understand agent/environment/model separation
- see why linear histories improve inspectability
- reason about bash-only action strategy
- identify where complexity should and should not live

## Design Characteristics

- minimal agent class and explicit control flow
- independent action execution via subprocess model
- linear message trajectories for easier debugging and FT/RL workflows

## Source References

- [Mini-SWE-Agent README: Minimal Architecture Notes](https://github.com/SWE-agent/mini-swe-agent/blob/main/README.md)
- [Default Agent Source](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py)
- [Local Environment Source](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/environments/local.py)

## Summary

You now understand how mini-swe-agent keeps performance and simplicity aligned.

Next: [Chapter 3: CLI, Batch, and Inspector Workflows](03-cli-batch-and-inspector-workflows.md)
