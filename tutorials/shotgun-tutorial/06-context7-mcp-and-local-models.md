---
layout: default
title: "Chapter 6: Context7 MCP and Local Models"
nav_order: 6
parent: Shotgun Tutorial
---

# Chapter 6: Context7 MCP and Local Models

Shotgun supports live documentation lookup through Context7 MCP and can run local-model workflows through Ollama integration.

## Context7 Integration

Context7 is attached as an MCP server for research flows so the agent can resolve library identifiers and fetch targeted docs during execution.

## Local Model Strategy

Ollama models are exposed via an OpenAI-compatible path with capability detection for tools and vision.

## Operational Caveats

- local models with weak tool-calling support may be constrained
- docs lookup requires external connectivity to the MCP endpoint
- model and provider choices should match task risk and latency budget

## Source References

- [Context7 Integration Architecture](https://github.com/shotgun-sh/shotgun/blob/main/docs/architecture/context7-mcp-integration.md)
- [Ollama/Local Models Architecture](https://github.com/shotgun-sh/shotgun/blob/main/docs/architecture/ollama-local-models.md)

## Summary

You now have a model for combining live docs retrieval and local-model execution pathways.

Next: [Chapter 7: Spec Sharing and Collaboration Workflows](07-spec-sharing-and-collaboration-workflows.md)
