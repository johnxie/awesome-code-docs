---
layout: default
title: "Chapter 1: Getting Started and Package Selection"
nav_order: 1
parent: MCP C# SDK Tutorial
---

# Chapter 1: Getting Started and Package Selection

This chapter establishes the right package boundary for your .NET MCP workload.

## Learning Goals

- pick between `ModelContextProtocol`, `.Core`, and `.AspNetCore`
- align package choice with hosting and transport requirements
- set baseline installation and first-run client/server validation
- avoid unnecessary dependency surface area

## Package Decision Guide

| Package | Best Fit |
|:--------|:---------|
| `ModelContextProtocol` | most projects using hosting + DI extensions |
| `ModelContextProtocol.Core` | minimal client/low-level server usage |
| `ModelContextProtocol.AspNetCore` | HTTP MCP server endpoints in ASP.NET Core |

## Baseline Setup

```bash
dotnet add package ModelContextProtocol --prerelease
```

Use `.AspNetCore` only when you need HTTP transport hosting; otherwise start with simpler stdio workflows.

## Source References

- [C# SDK Package Overview](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#packages)
- [Core Package README](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.Core/README.md)
- [AspNetCore Package README](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.AspNetCore/README.md)

## Summary

You now have a package-level starting point that fits your runtime shape.

Next: [Chapter 2: Client/Server Hosting and stdio Basics](02-client-server-hosting-and-stdio-basics.md)
