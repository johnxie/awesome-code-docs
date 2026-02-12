---
layout: default
title: "Chapter 8: Release Strategy and Production Operations"
nav_order: 8
parent: MCP Ext Apps Tutorial
---

# Chapter 8: Release Strategy and Production Operations

This chapter defines long-term operating practices for MCP Apps-based systems.

## Learning Goals

- align SDK releases with specification version controls
- manage app/host compatibility testing across updates
- set production safeguards for security, rendering, and message flow
- reduce breakage risk during spec or host behavior evolution

## Operations Controls

| Area | Baseline Control |
|:-----|:-----------------|
| spec compatibility | pin against stable spec revision and verify host support |
| release rollout | stage SDK updates with integration test gates |
| security posture | enforce sandbox, CSP, and context minimization |
| observability | capture host bridge errors and tool/UI mismatch metrics |

## Source References

- [Ext Apps Releases](https://github.com/modelcontextprotocol/ext-apps/releases)
- [Ext Apps README](https://github.com/modelcontextprotocol/ext-apps/blob/main/README.md)
- [MCP Apps Stable Spec](https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx)

## Summary

You now have a production operations framework for MCP Apps across app and host stacks.

Return to the [MCP Ext Apps Tutorial index](index.md).
