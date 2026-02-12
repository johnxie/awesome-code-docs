---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: GitHub MCP Server Tutorial
---

# Chapter 1: Getting Started

This chapter gets GitHub MCP connected with a minimum-risk initial setup.

## Learning Goals

- choose a quick path for first successful connection
- verify host compatibility and token prerequisites
- run a basic read operation to validate wiring
- avoid over-broad permissions during initial setup

## Fast Start Sequence

1. choose remote or local mode based on host support
2. configure MCP entry in your host with PAT/OAuth
3. run `list` or repository read actions first
4. verify tool visibility before enabling write workflows

## First Validation Checklist

- host sees the `github` MCP server
- auth flow succeeds
- read-only tools execute successfully
- no unexpected write-capable tools are exposed

## Source References

- [README](https://github.com/github/github-mcp-server/blob/main/README.md)
- [Installation Guides Index](https://github.com/github/github-mcp-server/tree/main/docs/installation-guides)

## Summary

You now have a safe baseline connection to GitHub MCP.

Next: [Chapter 2: Remote vs Local Architecture](02-remote-vs-local-architecture.md)
