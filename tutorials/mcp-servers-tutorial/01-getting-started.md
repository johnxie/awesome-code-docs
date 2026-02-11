---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: MCP Servers Tutorial
---

# Chapter 1: Getting Started

This chapter sets up a clean evaluation workflow for MCP reference servers.

## Clone and Inspect the Repository

```bash
git clone https://github.com/modelcontextprotocol/servers.git
cd servers
ls src
```

The `src/` directory contains each reference server implementation.

## Choose a Runtime Path

Most reference servers support multiple ways to run:

- package manager invocation (`npx`, `uvx`, or `pip`/`python -m` depending on server)
- Docker image execution
- editor/client-level MCP configuration

Use package-manager mode for local iteration and Docker mode when testing isolation and deploy parity.

## Recommended First Server

Start with `filesystem` or `time` because they are easy to validate and have clear I/O behavior.

Initial validation loop:

1. Register server in your MCP client config.
2. Ask the client to list tools.
3. Execute one read-only tool.
4. Execute one mutation tool in a safe sandbox.
5. Record behavior and error messages.

## Understand the Contract

Reference servers teach three things:

- request/response shapes for tools
- guardrail and safety patterns
- transport/runtime integration options

They are not optimized for your domain, data volume, or threat model out of the box.

## Baseline Evaluation Checklist

- What operations are read-only vs mutating?
- Which inputs can trigger side effects?
- How are paths/resources access-controlled?
- What metadata do you need for audit and traceability?
- Which parts must be replaced for production?

## Summary

You now have a repeatable method to evaluate each reference server safely.

Next: [Chapter 2: Filesystem Server](02-filesystem-server.md)
