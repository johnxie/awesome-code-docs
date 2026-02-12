---
layout: default
title: "Chapter 6: Signing, Verification, and Trust Controls"
nav_order: 6
parent: MCPB Tutorial
---

# Chapter 6: Signing, Verification, and Trust Controls

This chapter covers integrity and trust primitives in MCPB distribution.

## Learning Goals

- sign bundles with appropriate certificate chains
- verify signatures before publication and installation
- distinguish dev-time self-signed workflows from production trust models
- reduce supply-chain risk in host-side bundle acceptance

## Trust Workflow

| Step | Command |
|:-----|:--------|
| Sign | `mcpb sign` |
| Verify | `mcpb verify` |
| Inspect | `mcpb info` |
| Remove signature (dev-only) | `mcpb unsign` |

## Source References

- [MCPB CLI - Signing and Verification](https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md#mcpb-sign-mcpb-file)
- [MCPB CLI - Certificate Requirements](https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md#certificate-requirements)

## Summary

You now have a security-oriented workflow for trusted MCPB distribution.

Next: [Chapter 7: Examples, Language Patterns, and Distribution Readiness](07-examples-language-patterns-and-distribution-readiness.md)
