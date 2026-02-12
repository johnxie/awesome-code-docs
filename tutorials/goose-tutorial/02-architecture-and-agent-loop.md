---
layout: default
title: "Chapter 2: Architecture and Agent Loop"
nav_order: 2
parent: Goose Tutorial
---

# Chapter 2: Architecture and Agent Loop

This chapter explains how Goose turns requests into concrete engineering actions.

## Learning Goals

- understand Goose's core runtime components
- trace request -> tool call -> response loop behavior
- reason about context revision and token efficiency
- use this model to debug misbehavior faster

## Core Components

| Component | Role | Practical Impact |
|:----------|:-----|:-----------------|
| Interface (Desktop/CLI) | Collects prompts, shows outputs | Determines operator experience and control surface |
| Agent | Runs orchestration loop | Handles provider calls, tool invocations, and retries |
| Extensions (MCP) | Expose capabilities as tools | Enable shell, file, API, browser, memory, and more |

## Interactive Loop (Operational View)

1. user submits task
2. Goose sends task + available tools to model
3. model requests tool calls when needed
4. Goose executes tool calls and returns results
5. Goose revises context for relevance/token limits
6. model returns answer or next action request

## Why This Matters

- if outputs degrade, inspect tool surface and context length first
- if execution stalls, isolate whether provider/tool/permission is blocking
- if costs spike, tune context strategy and tool verbosity

## Error Handling Behavior

Goose treats many execution failures as recoverable signals to the model:

- malformed tool arguments
- unavailable tools
- command failures

This makes multi-step workflows more resilient than simple one-shot prompting.

## Source References

- [Goose Architecture](https://block.github.io/goose/docs/goose-architecture/)
- [Extensions Design](https://block.github.io/goose/docs/goose-architecture/extensions-design)

## Summary

You now have an operator-level mental model for Goose's execution loop and error paths.

Next: [Chapter 3: Providers and Model Routing](03-providers-and-model-routing.md)
