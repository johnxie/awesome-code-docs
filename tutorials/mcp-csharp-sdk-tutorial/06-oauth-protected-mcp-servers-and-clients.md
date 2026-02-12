---
layout: default
title: "Chapter 6: OAuth-Protected MCP Servers and Clients"
nav_order: 6
parent: MCP C# SDK Tutorial
---

# Chapter 6: OAuth-Protected MCP Servers and Clients

Protected MCP deployments in .NET require explicit server and client auth choreography.

## Learning Goals

- implement OAuth-protected MCP server endpoints in ASP.NET Core
- configure protected client flows for token acquisition and tool invocation
- validate scope/audience behavior in protected requests
- harden certificate and local dev environment flows for fewer auth surprises

## Security Implementation Checklist

1. protect MCP endpoints with JWT bearer auth and audience validation
2. expose OAuth protected resource metadata endpoint
3. enforce per-tool scope checks where blast radius differs
4. test client authorization-code flow against protected server repeatedly

## Source References

- [Protected MCP Server Sample](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/ProtectedMcpServer/README.md)
- [Protected MCP Client Sample](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/ProtectedMcpClient/README.md)
- [Security Policy](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/SECURITY.md)

## Summary

You now have a concrete pattern for securing C# MCP servers and clients with OAuth-aligned flows.

Next: [Chapter 7: Diagnostics, Versioning, and Breaking-Change Management](07-diagnostics-versioning-and-breaking-change-management.md)
