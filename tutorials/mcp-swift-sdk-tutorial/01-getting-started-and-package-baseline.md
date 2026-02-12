---
layout: default
title: "Chapter 1: Getting Started and Package Baseline"
nav_order: 1
parent: MCP Swift SDK Tutorial
---

# Chapter 1: Getting Started and Package Baseline

This chapter sets up a minimal, reproducible Swift MCP environment.

## Learning Goals

- configure Swift Package Manager dependencies correctly
- validate runtime prerequisites (Swift 6+, Xcode 16+)
- bootstrap a simple client/server setup before advanced features
- avoid mismatched SDK/protocol assumptions early

## Baseline Steps

1. add `swift-sdk` package dependency from tagged release
2. import `MCP` in target modules
3. run a minimal client connect flow
4. verify server capability negotiation output before feature development

## Source References

- [Swift SDK README - Installation](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md)
- [Swift SDK README - Requirements](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#requirements)

## Summary

You now have a stable Swift MCP baseline for subsequent client/server implementation.

Next: [Chapter 2: Client Transport and Capability Negotiation](02-client-transport-and-capability-negotiation.md)
