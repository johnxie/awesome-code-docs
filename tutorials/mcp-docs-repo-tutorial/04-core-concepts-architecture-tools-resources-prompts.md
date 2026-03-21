---
layout: default
title: "Chapter 4: Core Concepts: Architecture, Tools, Resources, Prompts"
nav_order: 4
parent: MCP Docs Repo Tutorial
---


# Chapter 4: Core Concepts: Architecture, Tools, Resources, Prompts

Welcome to **Chapter 4: Core Concepts: Architecture, Tools, Resources, Prompts**. In this part of **MCP Docs Repo Tutorial: Navigating the Archived MCP Documentation Repository**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on foundational conceptual guides that remain broadly useful.

## Learning Goals

- refresh protocol architecture and lifecycle model
- align tool/resource/prompt semantics across implementations
- apply concept docs when reviewing SDK-specific behavior
- avoid conceptual drift in internal docs and team onboarding

## Source References

- [Architecture Concepts](https://github.com/modelcontextprotocol/docs/blob/main/docs/concepts/architecture.mdx)
- [Tools Concepts](https://github.com/modelcontextprotocol/docs/blob/main/docs/concepts/tools.mdx)
- [Resources Concepts](https://github.com/modelcontextprotocol/docs/blob/main/docs/concepts/resources.mdx)
- [Prompts Concepts](https://github.com/modelcontextprotocol/docs/blob/main/docs/concepts/prompts.mdx)

## Summary

You now have a concept-level baseline for MCP system reasoning.

Next: [Chapter 5: Advanced Concepts: Transports, Sampling, and Roots](05-advanced-concepts-transports-sampling-and-roots.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `docs.json`

The `docs` module in [`docs.json`](https://github.com/modelcontextprotocol/docs/blob/HEAD/docs.json) handles a key part of this chapter's functionality:

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "willow",
  "name": "Model Context Protocol",
  "colors": {
    "primary": "#09090b",
    "light": "#FAFAFA",
    "dark": "#09090b"
  },
  "favicon": "/favicon.svg",
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "groups": [
          {
            "group": "Get Started",
            "pages": [
              "introduction",
              {
                "group": "Quickstart",
                "pages": [
                  "quickstart/server",
                  "quickstart/client",
                  "quickstart/user"
                ]
              },
              "examples",
              "clients"
            ]
          },
          {
            "group": "Tutorials",
            "pages": [
              "tutorials/building-mcp-with-llms",
```

This module is important because it defines how MCP Docs Repo Tutorial: Navigating the Archived MCP Documentation Repository implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[docs]
```
