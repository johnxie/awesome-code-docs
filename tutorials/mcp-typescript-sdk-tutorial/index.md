---
layout: default
title: "MCP TypeScript SDK Tutorial"
nav_order: 162
has_children: true
format_version: v2
---

# MCP TypeScript SDK Tutorial: Building and Migrating MCP Clients and Servers in TypeScript

> Learn how to use `modelcontextprotocol/typescript-sdk` to build production MCP clients and servers, migrate from v1 to v2 safely, and validate behavior with conformance workflows.

[![GitHub Repo](https://img.shields.io/badge/GitHub-modelcontextprotocol%2Ftypescript--sdk-black?logo=github)](https://github.com/modelcontextprotocol/typescript-sdk)
[![License](https://img.shields.io/badge/license-Apache--2.0%20transition-blue.svg)](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/modelcontextprotocol/typescript-sdk)](https://github.com/modelcontextprotocol/typescript-sdk/releases)

## Why This Track Matters

The TypeScript SDK is a core implementation surface for MCP in JavaScript/TypeScript ecosystems. It now spans split client/server/core packages, framework-specific middleware, and transport compatibility patterns that teams need to understand before shipping.

This track focuses on:

- choosing the right package and transport layers for your runtime
- implementing stable client and server flows across stdio and HTTP transports
- using advanced capabilities (sampling, elicitation, tasks) responsibly
- planning low-risk migration from v1 to v2 package and API boundaries

## Current Snapshot (Verified February 12, 2026)

- repository: [`modelcontextprotocol/typescript-sdk`](https://github.com/modelcontextprotocol/typescript-sdk)
- stars: about **11.6k**
- latest release: [`v1.26.0`](https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/v1.26.0) (**February 4, 2026**)
- recent activity: updated on **February 12, 2026**
- branch posture: `main` is v2 (pre-alpha), `v1.x` remains recommended for production during migration window
- licensing note: MCP project transition from MIT to Apache-2.0 (docs under CC-BY-4.0)

## Mental Model

```mermaid
flowchart LR
    A[App runtime] --> B[@modelcontextprotocol/client]
    A --> C[@modelcontextprotocol/server]
    B --> D[stdio, streamable-http, sse]
    C --> E[tools, resources, prompts]
    C --> F[middleware adapters]
    F --> G[Express, Hono, Node HTTP]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started and Package Model](01-getting-started-and-package-model.md) | Which SDK packages should I install first? | Correct baseline setup |
| [02 - Server Transports and Deployment Patterns](02-server-transports-and-deployment-patterns.md) | How should I design server runtime and transport layers? | Cleaner server architecture |
| [03 - Client Transports, OAuth, and Backwards Compatibility](03-client-transports-oauth-and-backwards-compatibility.md) | How do I connect clients across modern and legacy servers? | More resilient client behavior |
| [04 - Tool, Resource, Prompt Design and Completions](04-tool-resource-prompt-design-and-completions.md) | How should I model server capabilities for reliable client use? | Better interface quality |
| [05 - Sampling, Elicitation, and Experimental Tasks](05-sampling-elicitation-and-experimental-tasks.md) | When should I use advanced capability flows? | Safer advanced features |
| [06 - Middleware, Security, and Host Validation](06-middleware-security-and-host-validation.md) | How do I secure local and remote deployments? | Lower transport and host risk |
| [07 - v1 to v2 Migration Strategy](07-v1-to-v2-migration-strategy.md) | What migration plan minimizes breakage? | Predictable upgrade path |
| [08 - Conformance Testing and Contribution Workflows](08-conformance-testing-and-contribution-workflows.md) | How do teams verify and evolve SDK usage over time? | Long-term maintainability |

## What You Will Learn

- how to map SDK package boundaries to real deployment environments
- how to combine Streamable HTTP, stdio, and fallback patterns safely
- how to implement migration and compatibility strategy for active codebases
- how to validate behavior with conformance and integration testing loops

## Source References

- [TypeScript SDK README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md)
- [Server Docs](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/server.md)
- [Client Docs](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/client.md)
- [Capabilities Docs](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/capabilities.md)
- [Migration Guide](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/migration.md)
- [Server Examples](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/README.md)
- [Client Examples](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/client/README.md)
- [Conformance README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/test/conformance/README.md)

## Related Tutorials

- [MCP Python SDK Tutorial](../mcp-python-sdk-tutorial/)
- [MCP Inspector Tutorial](../mcp-inspector-tutorial/)
- [MCP Registry Tutorial](../mcp-registry-tutorial/)
- [MCP Use Tutorial](../mcp-use-tutorial/)

---

Start with [Chapter 1: Getting Started and Package Model](01-getting-started-and-package-model.md).
