---
layout: default
title: "Chapter 8: Production Governance and Release Strategy"
nav_order: 8
parent: GenAI Toolbox Tutorial
---

# Chapter 8: Production Governance and Release Strategy

This chapter closes with operating discipline for pre-1.0 and post-1.0 evolution.

## Learning Goals

- apply versioning expectations before and after stable release
- maintain security and secret handling standards in config and runtime
- define change-management gates for connector and tool updates
- keep documentation and operational runbooks synchronized

## Governance Playbook

1. pin runtime versions and document upgrade windows
2. gate schema/config changes through staged validation
3. monitor request behavior, failures, and connector-level drift
4. keep incident and rollback procedures tied to specific release versions
5. regularly revisit MCP versus SDK mode assumptions as requirements evolve

## Source References

- [README Versioning](https://github.com/googleapis/genai-toolbox/blob/main/README.md)
- [Developer Guide](https://github.com/googleapis/genai-toolbox/blob/main/DEVELOPER.md)
- [CHANGELOG](https://github.com/googleapis/genai-toolbox/blob/main/CHANGELOG.md)

## Summary

You now have an operational model for running GenAI Toolbox as production MCP database infrastructure.
