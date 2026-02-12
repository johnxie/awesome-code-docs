---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenSrc Tutorial
---

# Chapter 1: Getting Started

This chapter gets OpenSrc installed and fetching your first source dependency.

## Quick Start

```bash
npm install -g opensrc
opensrc zod
opensrc list
```

## Alternative Invocation

```bash
npx opensrc react react-dom
```

## What to Verify

- an `opensrc/` directory exists
- `opensrc/sources.json` is created
- `opensrc list` shows fetched entries

## Source References

- [OpenSrc README](https://github.com/vercel-labs/opensrc/blob/main/README.md)

## Summary

You now have OpenSrc running with an initial source import and index file.

Next: [Chapter 2: Input Parsing and Resolution Pipeline](02-input-parsing-and-resolution-pipeline.md)
