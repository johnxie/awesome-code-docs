---
layout: default
title: "Chapter 4: Host Bridge and Context Management"
nav_order: 4
parent: MCP Ext Apps Tutorial
---

# Chapter 4: Host Bridge and Context Management

This chapter explains host responsibilities for embedding and governing MCP Apps safely.

## Learning Goals

- understand host-side bridge package responsibilities
- manage context injection, messaging, and sandbox boundaries
- apply host-level UI/runtime constraints intentionally
- reduce security risk from over-broad host-app interfaces

## Host Responsibilities

| Responsibility | Why It Matters |
|:---------------|:---------------|
| resource resolution | maps tool-declared UI resources to renderable views |
| sandbox enforcement | isolates app execution and protects host environment |
| message brokering | enables controlled app-tool-host communication |
| context governance | limits exposed host/user data surface |

## Source References

- [Ext Apps README - For Host Developers](https://github.com/modelcontextprotocol/ext-apps/blob/main/README.md#for-host-developers)
- [Basic Host Example](https://github.com/modelcontextprotocol/ext-apps/blob/main/examples/basic-host/README.md)
- [MCP Apps Overview - Host Context/Security](https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/overview.md)

## Summary

You now have a host-bridge model for secure MCP Apps embedding.

Next: [Chapter 5: Patterns, Security, and Performance](05-patterns-security-and-performance.md)
