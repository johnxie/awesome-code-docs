---
layout: default
title: "Chapter 3: Tooling and Local Execution Boundaries"
nav_order: 3
parent: gptme Tutorial
---

# Chapter 3: Tooling and Local Execution Boundaries

gptme exposes tools for file editing, shell execution, web browsing, and more inside a local execution loop.

## Tooling Coverage

- shell and code execution
- file read/write/patch workflows
- web and browser access
- vision and multimodal context

## Boundary Strategy

- explicitly constrain tool allowlists for risky environments
- keep default confirmations enabled outside trusted automation jobs
- validate side effects with standard test/build commands

## Source References

- [gptme README: features and tools](https://github.com/gptme/gptme/blob/master/README.md)
- [Custom tool config docs](https://github.com/gptme/gptme/blob/master/docs/custom_tool.rst)

## Summary

You now understand how gptme's local tool loop works and how to control risk boundaries.

Next: [Chapter 4: Configuration Layers and Environment Strategy](04-configuration-layers-and-environment-strategy.md)
