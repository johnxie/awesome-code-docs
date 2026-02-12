---
layout: default
title: "Chapter 3: Client Transports and Connection Strategy"
nav_order: 3
parent: MCP Java SDK Tutorial
---

# Chapter 3: Client Transports and Connection Strategy

Client transport choice should match server topology and runtime constraints.

## Learning Goals

- choose transport strategy for local subprocess vs remote HTTP servers
- understand JDK HttpClient and Spring WebClient integration options
- plan reconnection and streaming behavior explicitly
- keep client capability handling predictable

## Transport Strategy Matrix

| Option | Best Fit | Primary Risk |
|:-------|:---------|:-------------|
| Stdio client transport | local tool servers launched by host process | process lifecycle fragility |
| JDK HTTP streamable transport | standard Java deployments without Spring | HTTP/session edge-case handling |
| Spring WebClient transport | Spring-native reactive apps | configuration spread across layers |

## Source References

- [Java SDK README - Client Transport Decisions](https://github.com/modelcontextprotocol/java-sdk/blob/main/README.md)
- [HttpClient Streamable Transport Class](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-core/src/main/java/io/modelcontextprotocol/client/transport/HttpClientStreamableHttpTransport.java)
- [Stdio Client Transport Class](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-core/src/main/java/io/modelcontextprotocol/client/transport/StdioClientTransport.java)
- [WebFlux Client Transport](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-spring/mcp-spring-webflux/src/main/java/io/modelcontextprotocol/client/transport/WebClientStreamableHttpTransport.java)

## Summary

You now have a transport selection framework for Java clients that balances simplicity and runtime resilience.

Next: [Chapter 4: Server Transports and Deployment Patterns](04-server-transports-and-deployment-patterns.md)
