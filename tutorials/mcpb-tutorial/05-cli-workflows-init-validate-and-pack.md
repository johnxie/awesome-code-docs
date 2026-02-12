---
layout: default
title: "Chapter 5: CLI Workflows: Init, Validate, and Pack"
nav_order: 5
parent: MCPB Tutorial
---

# Chapter 5: CLI Workflows: Init, Validate, and Pack

This chapter standardizes practical CLI workflows for bundle creation.

## Learning Goals

- use `mcpb init` to bootstrap valid manifests quickly
- validate manifests before packaging and distribution
- pack deterministic `.mcpb` archives with appropriate exclusions
- integrate `.mcpbignore` into repeatable build pipelines

## Core Command Flow

1. `mcpb init` to scaffold manifest
2. `mcpb validate` against schema
3. `mcpb pack` for distributable archive
4. `mcpb info` for metadata inspection

## Source References

- [MCPB CLI Documentation](https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md)
- [MCPB README - For Bundle Developers](https://github.com/modelcontextprotocol/mcpb/blob/main/README.md#for-bundle-developers)

## Summary

You now have a repeatable packaging workflow for MCPB bundle production.

Next: [Chapter 6: Signing, Verification, and Trust Controls](06-signing-verification-and-trust-controls.md)
