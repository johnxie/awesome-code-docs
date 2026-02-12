---
layout: default
title: "Chapter 2: Architecture and Control Plane"
nav_order: 2
parent: GenAI Toolbox Tutorial
---

# Chapter 2: Architecture and Control Plane

This chapter explains how Toolbox sits between agent frameworks and data systems.

## Learning Goals

- map the control-plane role of Toolbox in agent architectures
- understand why config-driven tool definitions reduce redeploy friction
- separate orchestration concerns from database execution concerns
- reason about shared tool reuse across multiple agents and apps

## Architecture Summary

Toolbox centralizes source and tool definitions, then exposes them to clients through consistent runtime interfaces. This lets teams evolve tooling and access patterns without continually rewriting integration code.

## Source References

- [README Architecture Section](https://github.com/googleapis/genai-toolbox/blob/main/README.md)
- [Introduction Docs](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/getting-started/introduction/_index.md)

## Summary

You now understand how Toolbox provides a reusable orchestration layer for database-aware agents.

Next: [Chapter 3: `tools.yaml`: Sources, Tools, Toolsets, Prompts](03-tools-yaml-sources-tools-toolsets-prompts.md)
