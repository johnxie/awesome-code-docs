---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Claude Plugins Official Tutorial
---

# Chapter 1: Getting Started

This chapter gets you installing and running plugins from the official directory.

## Learning Goals

- connect Claude Code to the official plugin directory
- install one internal plugin and validate command availability
- inspect plugin metadata and initial behavior
- establish baseline trust checks before daily use

## Install Flow

In Claude Code:

```text
/plugin install {plugin-name}@claude-plugin-directory
```

You can also discover plugins through:

```text
/plugin
```

## First Validation Steps

- install a focused plugin (for example `code-review`)
- run one documented command from that plugin
- verify expected behavior and output quality
- remove or disable plugins that are not immediately useful

## Source References

- [Directory README Installation](https://github.com/anthropics/claude-plugins-official/blob/main/README.md#installation)
- [Code Review Plugin Example](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review)
- [Official Plugin Docs](https://code.claude.com/docs/en/plugins)

## Summary

You now have a working baseline for installing and using directory plugins.

Next: [Chapter 2: Directory Architecture and Marketplace Model](02-directory-architecture-and-marketplace-model.md)
