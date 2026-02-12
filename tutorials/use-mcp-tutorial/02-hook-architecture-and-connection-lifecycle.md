---
layout: default
title: "Chapter 2: Hook Architecture and Connection Lifecycle"
nav_order: 2
parent: use-mcp Tutorial
---

# Chapter 2: Hook Architecture and Connection Lifecycle

This chapter explains core `useMcp` lifecycle and state transitions.

## Learning Goals

- understand lifecycle states (`discovering` to `ready`/`failed`)
- model UI behavior around connection phases
- use imperative controls (`retry`, `disconnect`, `authenticate`) safely
- avoid race conditions in component-driven connection flows

## Lifecycle States

| State | Meaning |
|:------|:--------|
| discovering / connecting / loading | initialization and capability loading |
| pending_auth / authenticating | auth flow in progress |
| ready | operations available |
| failed | terminal error until retry/authentication |

## Source References

- [use-mcp README - API Reference](https://github.com/modelcontextprotocol/use-mcp/blob/main/README.md#api-reference)
- [React Integration README](https://github.com/modelcontextprotocol/use-mcp/blob/main/src/react/README.md)

## Summary

You now have a lifecycle model for robust hook-driven MCP client UX.

Next: [Chapter 3: Authentication, OAuth Callback, and Storage](03-authentication-oauth-callback-and-storage.md)
