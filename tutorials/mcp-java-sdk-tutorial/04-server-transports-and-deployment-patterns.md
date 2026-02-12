---
layout: default
title: "Chapter 4: Server Transports and Deployment Patterns"
nav_order: 4
parent: MCP Java SDK Tutorial
---

# Chapter 4: Server Transports and Deployment Patterns

Server transport architecture should be explicit before production rollout.

## Learning Goals

- deploy servlet, WebFlux, or WebMVC server transports based on environment
- understand streamable HTTP provider boundaries
- apply stateless vs sessioned behavior intentionally
- reduce deployment risk by isolating transport concerns

## Deployment Patterns

- embedded servlet transport for portable Java server deployments
- Spring WebFlux for reactive pipelines and non-blocking APIs
- Spring WebMVC for established servlet-style Spring applications
- stdio server provider for local/desktop-oriented integrations

## Source References

- [Conformance Servlet Server README](https://github.com/modelcontextprotocol/java-sdk/blob/main/conformance-tests/server-servlet/README.md)
- [HttpServlet Streamable Transport Provider](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-core/src/main/java/io/modelcontextprotocol/server/transport/HttpServletStreamableServerTransportProvider.java)
- [WebFlux Server Transport Provider](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-spring/mcp-spring-webflux/src/main/java/io/modelcontextprotocol/server/transport/WebFluxStreamableServerTransportProvider.java)
- [WebMVC Server Transport README](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-spring/mcp-spring-webmvc/README.md)

## Summary

You now have deployment-level transport guidance for selecting the right Java runtime surface.

Next: [Chapter 5: Tools, Resources, Prompts, and Schema Validation](05-tools-resources-prompts-and-schema-validation.md)
