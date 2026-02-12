---
layout: default
title: "Chapter 1: Getting Started and Stack Selection"
nav_order: 1
parent: MCP Use Tutorial
---

# Chapter 1: Getting Started and Stack Selection

This chapter helps you choose the right starting workflow between Python and TypeScript.

## Learning Goals

- understand mcp-use stack components (agent, client, server, inspector)
- choose initial language path by project constraints
- run the fastest first agent/client flow
- identify when to switch from local quickstart to production setup

## Start Decision Heuristic

| Team Profile | Best Starting Path |
|:-------------|:-------------------|
| Python-heavy ML/app team | Python quickstart + agent/client stack |
| TypeScript web/product team | TypeScript quickstart + server framework |
| Mixed-stack platform team | start with shared client config model, then split by runtime |

## Source References

- [Main README](https://github.com/mcp-use/mcp-use/blob/main/README.md)
- [TypeScript Quickstart](https://github.com/mcp-use/mcp-use/blob/main/docs/typescript/getting-started/quickstart.mdx)
- [Python Quickstart](https://github.com/mcp-use/mcp-use/blob/main/docs/python/getting-started/quickstart.mdx)

## Summary

You now have a clear stack-entry decision for mcp-use adoption.

Next: [Chapter 2: Client Configuration, Sessions, and Transport Choices](02-client-configuration-sessions-and-transport-choices.md)
