---
layout: default
title: "Chapter 3: ASP.NET Core HTTP Transport and Session Routing"
nav_order: 3
parent: MCP C# SDK Tutorial
---

# Chapter 3: ASP.NET Core HTTP Transport and Session Routing

HTTP deployment patterns in C# should be explicit about route scoping and per-session behavior.

## Learning Goals

- deploy MCP endpoints with ASP.NET Core integration
- design per-route/per-session tool availability safely
- avoid overexposing tool catalogs across endpoint surfaces
- align HTTP topology with policy and tenant boundaries

## Route and Session Strategy

- expose focused MCP routes for distinct tool domains when possible
- keep all-tools endpoints gated and monitored
- use route-aware filtering for session-specific tool narrowing
- document endpoint semantics so clients can discover expected capability scope

## Source References

- [AspNetCore Package README](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.AspNetCore/README.md)
- [Per-Session Tools Sample](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/AspNetCoreMcpPerSessionTools/README.md)
- [Docs Concepts - HTTP Context](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/httpcontext/httpcontext.md)

## Summary

You now have an HTTP architecture model for route-scoped MCP services in ASP.NET Core.

Next: [Chapter 4: Tools, Prompts, Resources, and Filter Pipelines](04-tools-prompts-resources-and-filter-pipelines.md)
