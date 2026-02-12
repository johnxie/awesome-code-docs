---
layout: default
title: "Chapter 2: Directory Architecture and Marketplace Model"
nav_order: 2
parent: Claude Plugins Official Tutorial
---

# Chapter 2: Directory Architecture and Marketplace Model

This chapter explains the repository layout and curation model.

## Learning Goals

- distinguish internal plugins from external partner/community plugins
- understand how marketplace metadata is structured
- navigate plugin directories for capability discovery
- map directory structure to operational decisions

## Repository Topology

- `plugins/`: internal plugins maintained by Anthropic
- `external_plugins/`: third-party and partner plugins
- `.claude-plugin/marketplace.json`: marketplace-level catalog metadata

## Operational Implications

- internal plugins may align closely with official guidance patterns
- external plugins increase capability breadth but require stronger vetting
- marketplace metadata is the central source of installable plugin inventory

## Source References

- [Directory README Structure](https://github.com/anthropics/claude-plugins-official/blob/main/README.md#structure)
- [Marketplace Catalog](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)
- [Internal Plugins Directory](https://github.com/anthropics/claude-plugins-official/tree/main/plugins)
- [External Plugins Directory](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins)

## Summary

You now understand the curation and architecture layers of the directory.

Next: [Chapter 3: Plugin Manifest and Structural Contracts](03-plugin-manifest-and-structural-contracts.md)
