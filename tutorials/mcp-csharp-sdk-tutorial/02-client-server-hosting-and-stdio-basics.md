---
layout: default
title: "Chapter 2: Client/Server Hosting and stdio Basics"
nav_order: 2
parent: MCP C# SDK Tutorial
---

# Chapter 2: Client/Server Hosting and stdio Basics

This chapter covers practical onboarding for clients and servers using standard .NET hosting patterns.

## Learning Goals

- build a client with `McpClient.CreateAsync` and stdio transport
- bootstrap a server with host builder + tool discovery from assemblies
- wire logging to stderr for protocol-safe stdio behavior
- understand where low-level server handlers fit when you need more control

## Hosting Flow

1. instantiate transport (`StdioClientTransport` or stdio server transport)
2. create client/server using SDK host abstractions
3. register tools/prompts/resources through attributes or explicit handlers
4. run server and verify tool list/call paths end to end

## Source References

- [C# SDK README - Getting Started Client/Server](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md)
- [Core README - Client/Server](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.Core/README.md)

## Summary

You now have a working stdio baseline for .NET MCP development.

Next: [Chapter 3: ASP.NET Core HTTP Transport and Session Routing](03-aspnetcore-http-transport-and-session-routing.md)
