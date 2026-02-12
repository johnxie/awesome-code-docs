---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Everything Claude Code Tutorial
---

# Chapter 1: Getting Started

This chapter gets the package installed and verifies first workflow execution.

## Learning Goals

- install the marketplace plugin correctly
- install required rules for your language stack
- run initial commands and confirm capability surfaces
- avoid common first-run setup errors

## Quick Install

In Claude Code:

```bash
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

Then install rules from the repo clone:

```bash
./install.sh typescript
```

## First Validation

- run `/plan "small feature"`
- run `/code-review` on a branch with sample changes
- run `/verify` for basic quality pass

## Source References

- [README Quick Start](https://github.com/affaan-m/everything-claude-code/blob/main/README.md#-quick-start)
- [Rules Install Guide](https://github.com/affaan-m/everything-claude-code/blob/main/rules/README.md#installation)

## Summary

You now have a functioning baseline configuration.

Next: [Chapter 2: Architecture and Component Topology](02-architecture-and-component-topology.md)
