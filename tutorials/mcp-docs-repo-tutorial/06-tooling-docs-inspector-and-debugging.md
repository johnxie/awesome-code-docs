---
layout: default
title: "Chapter 6: Tooling Docs: Inspector and Debugging"
nav_order: 6
parent: MCP Docs Repo Tutorial
---


# Chapter 6: Tooling Docs: Inspector and Debugging

Welcome to **Chapter 6: Tooling Docs: Inspector and Debugging**. In this part of **MCP Docs Repo Tutorial: Navigating the Archived MCP Documentation Repository**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter extracts practical debugging workflows from archived tooling guides.

## Learning Goals

- apply inspector usage patterns for server validation
- use debugging workflows for Claude Desktop and local server diagnostics
- structure logs and troubleshooting steps for faster issue resolution
- translate archived guidance to current tooling versions safely

## Source References

- [Inspector Guide](https://github.com/modelcontextprotocol/docs/blob/main/docs/tools/inspector.mdx)
- [Debugging Guide](https://github.com/modelcontextprotocol/docs/blob/main/docs/tools/debugging.mdx)

## Summary

You now have a tooling-oriented debugging model grounded in MCP documentation guidance.

Next: [Chapter 7: Tutorial Assets and Client Ecosystem Matrix](07-tutorial-assets-and-client-ecosystem-matrix.md)

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
