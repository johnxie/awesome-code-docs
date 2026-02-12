---
layout: default
title: "Chapter 6: Security, Authorization, and Runtime Controls"
nav_order: 6
parent: MCP Java SDK Tutorial
---

# Chapter 6: Security, Authorization, and Runtime Controls

Java SDK security posture depends on transport controls and host-level authorization integration.

## Learning Goals

- apply transport-level security validators for HTTP deployments
- integrate authorization through framework-native controls
- align runtime behavior with MCP security best practices
- avoid weak defaults around origin and session handling

## Security Principles

- enforce origin/session protections in HTTP transport providers
- keep authorization hooks pluggable to fit existing security stacks
- treat server tool/resource scope as least-privilege surfaces
- log security-relevant events with enough context for incident triage

## Source References

- [Security Policy](https://github.com/modelcontextprotocol/java-sdk/blob/main/SECURITY.md)
- [Server Transport Security Validator](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-core/src/main/java/io/modelcontextprotocol/server/transport/ServerTransportSecurityValidator.java)
- [Default Security Validator](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-core/src/main/java/io/modelcontextprotocol/server/transport/DefaultServerTransportSecurityValidator.java)
- [Contributing - Security Section](https://github.com/modelcontextprotocol/java-sdk/blob/main/CONTRIBUTING.md)

## Summary

You now have a security baseline for Java MCP services that is compatible with framework-specific auth policies.

Next: [Chapter 7: Conformance Testing and Quality Workflows](07-conformance-testing-and-quality-workflows.md)
