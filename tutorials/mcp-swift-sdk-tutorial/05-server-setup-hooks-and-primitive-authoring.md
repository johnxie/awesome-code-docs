---
layout: default
title: "Chapter 5: Server Setup, Hooks, and Primitive Authoring"
nav_order: 5
parent: MCP Swift SDK Tutorial
---

# Chapter 5: Server Setup, Hooks, and Primitive Authoring

This chapter covers core server composition for Swift MCP services.

## Learning Goals

- bootstrap a server with clear lifecycle boundaries
- implement tools/resources/prompts with consistent schemas and behavior
- use initialize hooks for startup-time policy/config checks
- avoid tight coupling between transport plumbing and domain logic

## Server Build Steps

1. initialize server with implementation metadata
2. register tools/resources/prompts in coherent domains
3. add initialize hook for capability and policy checks
4. test all primitive flows before exposing HTTP endpoints

## Source References

- [Swift SDK README - Server Usage](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#server-usage)
- [Swift SDK README - Initialize Hook](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#initialize-hook)

## Summary

You now have a structured foundation for implementing Swift MCP servers.

Next: [Chapter 6: Transports, Custom Implementations, and Shutdown](06-transports-custom-implementations-and-shutdown.md)
