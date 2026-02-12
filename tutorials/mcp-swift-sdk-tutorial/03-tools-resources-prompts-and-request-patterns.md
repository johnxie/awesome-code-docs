---
layout: default
title: "Chapter 3: Tools, Resources, Prompts, and Request Patterns"
nav_order: 3
parent: MCP Swift SDK Tutorial
---

# Chapter 3: Tools, Resources, Prompts, and Request Patterns

This chapter maps common MCP primitive interactions to Swift client usage patterns.

## Learning Goals

- list and invoke tools with typed argument handling
- read and subscribe to resources where available
- fetch prompts with argument expansion reliably
- manage content-type handling across text/image/audio/resource returns

## Usage Guidance

- centralize primitive invocation wrappers for consistency
- validate argument and response assumptions before UI consumption
- treat resource subscriptions as stateful flows requiring explicit lifecycle handling
- keep prompt retrieval separate from model execution logic

## Source References

- [Swift SDK README - Tools](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#tools)
- [Swift SDK README - Resources](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#resources)
- [Swift SDK README - Prompts](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#prompts)

## Summary

You now have a predictable pattern for primitive interactions in Swift MCP clients.

Next: [Chapter 4: Sampling, Human-in-the-Loop, and Error Handling](04-sampling-human-in-the-loop-and-error-handling.md)
