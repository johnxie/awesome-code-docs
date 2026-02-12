---
layout: default
title: "MCPB Tutorial"
nav_order: 174
has_children: true
format_version: v2
---

# MCPB Tutorial: Packaging and Distributing Local MCP Servers as Bundles

> Learn how to use `modelcontextprotocol/mcpb` to package local MCP servers into signed `.mcpb` bundles with manifest metadata, CLI workflows, and distribution-ready operational controls.

[![GitHub Repo](https://img.shields.io/badge/GitHub-modelcontextprotocol%2Fmcpb-black?logo=github)](https://github.com/modelcontextprotocol/mcpb)
[![npm](https://img.shields.io/npm/v/@anthropic-ai/mcpb)](https://www.npmjs.com/package/@anthropic-ai/mcpb)
[![Latest Release](https://img.shields.io/github/v/release/modelcontextprotocol/mcpb)](https://github.com/modelcontextprotocol/mcpb/releases)

## Why This Track Matters

As MCP servers proliferate, teams need a consistent packaging format for local installation, updates, and trust validation. MCP Bundles (`.mcpb`) provide a portable distribution layer that packages server runtime files with a manifest-driven install contract.

This track focuses on:

- understanding the DXT -> MCPB rename and format model
- authoring high-quality `manifest.json` definitions
- operating CLI workflows for init, validate, pack, sign, and verify
- planning secure distribution and host compatibility controls

## Current Snapshot (Verified February 12, 2026)

- repository: [`modelcontextprotocol/mcpb`](https://github.com/modelcontextprotocol/mcpb)
- stars: about **1.7k**
- latest release: [`v2.1.2`](https://github.com/modelcontextprotocol/mcpb/releases/tag/v2.1.2) (**December 4, 2025**)
- recent activity: updated on **February 12, 2026**
- package baseline: `npm install -g @anthropic-ai/mcpb`
- format note: `.dxt` tooling was renamed to `.mcpb`; update legacy references accordingly
- license: MIT

## Mental Model

```mermaid
flowchart LR
    A[Local MCP server code] --> B[manifest.json]
    B --> C[mcpb validate]
    C --> D[mcpb pack]
    D --> E[extension.mcpb]
    E --> F[mcpb sign/verify]
    F --> G[Host install + runtime]
```

## Chapter Guide

| Chapter | Key Question | Outcome |
|:--------|:-------------|:--------|
| [01 - Getting Started and Bundle Fundamentals](01-getting-started-and-bundle-fundamentals.md) | What is MCPB and how do I start building bundles? | Fast onboarding |
| [02 - Manifest Model, Metadata, and Compatibility](02-manifest-model-metadata-and-compatibility.md) | How should `manifest.json` be structured for durable installs? | Better compatibility |
| [03 - Server Configuration and Runtime Packaging](03-server-configuration-and-runtime-packaging.md) | How do Node/Python/Binary/UV runtime options affect bundle design? | Safer runtime choices |
| [04 - Tools, Prompts, User Config, and Localization](04-tools-prompts-user-config-and-localization.md) | How do I model capabilities and user-configurable inputs cleanly? | Higher UX quality |
| [05 - CLI Workflows: Init, Validate, and Pack](05-cli-workflows-init-validate-and-pack.md) | How do I standardize bundle creation pipelines? | Repeatable packaging |
| [06 - Signing, Verification, and Trust Controls](06-signing-verification-and-trust-controls.md) | How do I ship bundles with integrity guarantees? | Stronger supply-chain posture |
| [07 - Examples, Language Patterns, and Distribution Readiness](07-examples-language-patterns-and-distribution-readiness.md) | What do practical bundle implementations look like? | Faster productionization |
| [08 - Release, Governance, and Ecosystem Operations](08-release-governance-and-ecosystem-operations.md) | How do teams operate MCPB workflows at scale over time? | Durable operations |

## What You Will Learn

- how to design bundle manifests that balance flexibility and compatibility
- how to choose runtime packaging strategies per language and environment
- how to run signed, verifiable distribution flows for local MCP servers
- how to implement governance controls around updates and host trust

## Source References

- [MCPB README](https://github.com/modelcontextprotocol/mcpb/blob/main/README.md)
- [MCPB Manifest Spec](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md)
- [MCPB CLI Documentation](https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md)
- [MCPB Examples](https://github.com/modelcontextprotocol/mcpb/blob/main/examples/README.md)
- [Hello World UV Example](https://github.com/modelcontextprotocol/mcpb/blob/main/examples/hello-world-uv/README.md)
- [MCPB Contributing Guide](https://github.com/modelcontextprotocol/mcpb/blob/main/CONTRIBUTING.md)

## Related Tutorials

- [MCP Specification Tutorial](../mcp-specification-tutorial/)
- [MCP Servers Tutorial](../mcp-servers-tutorial/)
- [MCP Ext Apps Tutorial](../mcp-ext-apps-tutorial/)
- [MCP Use Tutorial](../mcp-use-tutorial/)

---

Start with [Chapter 1: Getting Started and Bundle Fundamentals](01-getting-started-and-bundle-fundamentals.md).
