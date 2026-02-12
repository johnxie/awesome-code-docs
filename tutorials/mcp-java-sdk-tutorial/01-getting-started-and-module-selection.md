---
layout: default
title: "Chapter 1: Getting Started and Module Selection"
nav_order: 1
parent: MCP Java SDK Tutorial
---

# Chapter 1: Getting Started and Module Selection

This chapter establishes a clean dependency and runtime baseline for Java MCP projects.

## Learning Goals

- choose between `mcp`, `mcp-core`, and Spring modules
- align Java version and build tooling prerequisites
- avoid premature coupling to one transport or framework layer
- set up reproducible local build/test flows

## Module Selection Guide

| Module | Use When |
|:-------|:---------|
| `mcp` | you want the convenience bundle for most workloads |
| `mcp-core` | you need lower-level control and minimal dependencies |
| `mcp-spring` | you are integrating with Spring WebFlux/WebMVC stacks |

## First-Run Steps

1. confirm Java 17+ and Maven wrapper availability
2. start with `mcp` unless you have a strict minimal-dependency requirement
3. run `./mvnw clean install -DskipTests` to validate baseline build
4. move to module-specific integrations only after client/server flows work

## Source References

- [Java SDK README](https://github.com/modelcontextprotocol/java-sdk/blob/main/README.md)
- [mcp Module README](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp/README.md)
- [Contributing Prerequisites](https://github.com/modelcontextprotocol/java-sdk/blob/main/CONTRIBUTING.md)

## Summary

You now have a stable Java MCP baseline and module decision model.

Next: [Chapter 2: SDK Architecture: Reactive Model and JSON Layer](02-sdk-architecture-reactive-model-and-json-layer.md)
