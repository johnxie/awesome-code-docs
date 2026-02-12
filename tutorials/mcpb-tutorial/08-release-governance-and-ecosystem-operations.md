---
layout: default
title: "Chapter 8: Release, Governance, and Ecosystem Operations"
nav_order: 8
parent: MCPB Tutorial
---

# Chapter 8: Release, Governance, and Ecosystem Operations

This chapter defines long-term governance controls for operating MCPB workflows across teams.

## Learning Goals

- align release practices with manifest and runtime compatibility policies
- standardize CI checks for validation/signature quality gates
- manage migration messaging and backward compatibility across bundle versions
- integrate contribution guidelines into sustainable maintenance loops

## Operations Checklist

1. enforce `validate -> pack -> sign -> verify` in CI pipelines
2. maintain compatibility matrices per target host/client
3. version manifests and server runtime contracts deliberately
4. document contributor and release procedures for maintainers

## Source References

- [MCPB README - Release Process](https://github.com/modelcontextprotocol/mcpb/blob/main/README.md#release-process)
- [MCPB Contributing Guide](https://github.com/modelcontextprotocol/mcpb/blob/main/CONTRIBUTING.md)
- [MCPB Releases](https://github.com/modelcontextprotocol/mcpb/releases)

## Summary

You now have a governance model for operating MCPB packaging and distribution at scale.

Return to the [MCPB Tutorial index](index.md).
