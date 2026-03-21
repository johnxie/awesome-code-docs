---
layout: default
title: "Chapter 1: Getting Started and Archive Context"
nav_order: 1
parent: MCP Docs Repo Tutorial
---


# Chapter 1: Getting Started and Archive Context

Welcome to **Chapter 1: Getting Started and Archive Context**. In this part of **MCP Docs Repo Tutorial: Navigating the Archived MCP Documentation Repository**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter defines the current role of the archived docs repository.

## Learning Goals

- identify the archive status and practical implications
- map when archived docs are useful vs when active docs are required
- avoid treating archived content as authoritative for new protocol changes
- establish source-of-truth expectations for your team

## Source References

- [Docs Repository README](https://github.com/modelcontextprotocol/docs/blob/main/README.md)
- [Canonical Docs Location](https://github.com/modelcontextprotocol/modelcontextprotocol/tree/main/docs)

## Summary

You now have a clear scope boundary for using archived docs safely.

Next: [Chapter 2: Repository Layout and Canonical Migration Path](02-repository-layout-and-canonical-migration-path.md)

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
