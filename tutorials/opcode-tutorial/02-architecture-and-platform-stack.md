---
layout: default
title: "Chapter 2: Architecture and Platform Stack"
nav_order: 2
parent: Opcode Tutorial
---

# Chapter 2: Architecture and Platform Stack

This chapter covers the technical foundation behind Opcode's desktop experience.

## Learning Goals

- understand frontend/backend responsibilities
- map Tauri + React + Rust architecture to runtime behavior
- reason about storage and process boundaries
- align architecture with debugging strategy

## Stack Overview

| Layer | Technology |
|:------|:-----------|
| desktop shell | Tauri 2 |
| frontend | React 18 + TypeScript + Vite |
| backend/runtime | Rust |
| storage | SQLite |
| package tooling | Bun |

## Architecture Implications

- desktop-native distribution with web-style UX
- strong Rust-based process and state control
- straightforward contributor model for frontend/backend changes

## Source References

- [Opcode README: Tech Stack](https://github.com/winfunc/opcode/blob/main/README.md#tech-stack)
- [Opcode README: Project Structure](https://github.com/winfunc/opcode/blob/main/README.md#project-structure)

## Summary

You now understand the core architecture choices that shape Opcode behavior.

Next: [Chapter 3: Projects and Session Management](03-projects-and-session-management.md)
