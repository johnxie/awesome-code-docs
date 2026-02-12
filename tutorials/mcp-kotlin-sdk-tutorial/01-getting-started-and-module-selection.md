---
layout: default
title: "Chapter 1: Getting Started and Module Selection"
nav_order: 1
parent: MCP Kotlin SDK Tutorial
---

# Chapter 1: Getting Started and Module Selection

This chapter sets a clean dependency and runtime baseline for Kotlin MCP projects.

## Learning Goals

- choose the right artifact strategy (`kotlin-sdk` vs client/server splits)
- align Kotlin/JVM/Ktor prerequisites before protocol implementation
- establish a reproducible first-run workflow
- avoid hidden transport dependency gaps

## Module Selection Matrix

| Artifact | Use When |
|:---------|:---------|
| `kotlin-sdk` | you want client + server APIs together |
| `kotlin-sdk-client` | you only build MCP clients |
| `kotlin-sdk-server` | you only expose MCP server primitives |

## Baseline Steps

1. confirm Kotlin 2.2+ toolchain and JVM 11+ runtime
2. add Maven Central and one of the SDK artifacts
3. add explicit Ktor engine dependencies for your transport needs
4. run one sample flow (client or server) before adding custom features

## Source References

- [Kotlin SDK README - Installation](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/README.md#installation)
- [Kotlin SDK README - Ktor Dependencies](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/README.md#ktor-dependencies)
- [Client Sample README](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/samples/kotlin-mcp-client/README.md)

## Summary

You now have a stable Kotlin baseline and module selection model.

Next: [Chapter 2: Core Protocol Model and Module Architecture](02-core-protocol-model-and-module-architecture.md)
