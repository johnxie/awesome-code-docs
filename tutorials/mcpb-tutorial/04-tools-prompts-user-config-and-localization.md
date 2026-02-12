---
layout: default
title: "Chapter 4: Tools, Prompts, User Config, and Localization"
nav_order: 4
parent: MCPB Tutorial
---

# Chapter 4: Tools, Prompts, User Config, and Localization

This chapter covers how bundles declare capability surfaces and user-facing configuration.

## Learning Goals

- declare static tools/prompts and generated capability flags safely
- design `user_config` schemas with validation and sensitive field handling
- apply localization resources for user-facing metadata
- keep host UX predictable across locales and environments

## Configuration Guardrails

1. define user config with explicit type and validation constraints
2. mark sensitive fields (`api_key`, tokens) appropriately
3. avoid localization gaps for primary user-facing metadata
4. keep generated capability declarations aligned with runtime behavior

## Source References

- [Manifest Spec - User Configuration](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md#user-configuration)
- [Manifest Spec - Tools and Prompts](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md#tools-and-prompts)
- [Manifest Spec - Localization](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md#localization)

## Summary

You now have a configuration and localization strategy for robust bundle UX.

Next: [Chapter 5: CLI Workflows: Init, Validate, and Pack](05-cli-workflows-init-validate-and-pack.md)
