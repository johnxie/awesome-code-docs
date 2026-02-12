---
layout: default
title: "Chapter 1: Getting Started and Bundle Fundamentals"
nav_order: 1
parent: MCPB Tutorial
---

# Chapter 1: Getting Started and Bundle Fundamentals

This chapter introduces MCPB purpose, terminology, and first-run setup.

## Learning Goals

- understand the MCPB package format and distribution model
- account for DXT-to-MCPB naming migration in tooling/docs
- install CLI and run first bundle scaffolding workflow
- align local server packaging expectations before implementation

## Baseline Setup

```bash
npm install -g @anthropic-ai/mcpb
```

Then initialize a bundle directory with `mcpb init`, define `manifest.json`, and produce a first archive via `mcpb pack`.

## Source References

- [MCPB README](https://github.com/modelcontextprotocol/mcpb/blob/main/README.md)
- [MCPB CLI - Installation](https://github.com/modelcontextprotocol/mcpb/blob/main/CLI.md#installation)

## Summary

You now have a baseline model for creating MCP bundles from local server projects.

Next: [Chapter 2: Manifest Model, Metadata, and Compatibility](02-manifest-model-metadata-and-compatibility.md)
