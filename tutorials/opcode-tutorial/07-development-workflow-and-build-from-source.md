---
layout: default
title: "Chapter 7: Development Workflow and Build from Source"
nav_order: 7
parent: Opcode Tutorial
---

# Chapter 7: Development Workflow and Build from Source

This chapter covers contributor workflows and cross-platform source builds.

## Learning Goals

- set up Rust + Bun + system dependencies
- run local dev and production builds
- execute core quality checks
- troubleshoot common build failures

## Core Commands

```bash
bun install
bun run tauri dev
bun run tauri build
```

Additional quality commands:

- `bunx tsc --noEmit`
- `cd src-tauri && cargo test`
- `cd src-tauri && cargo fmt`

## Source References

- [Opcode README: Build from Source](https://github.com/winfunc/opcode/blob/main/README.md#-build-from-source)
- [Opcode README: Development Commands](https://github.com/winfunc/opcode/blob/main/README.md#development-commands)

## Summary

You now have a full contributor baseline for building and validating Opcode.

Next: [Chapter 8: Production Operations and Security](08-production-operations-and-security.md)
