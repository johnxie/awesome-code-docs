---
layout: default
title: "Chapter 2: Manifest Model, Metadata, and Compatibility"
nav_order: 2
parent: MCPB Tutorial
---

# Chapter 2: Manifest Model, Metadata, and Compatibility

This chapter explains `manifest.json` as the bundle contract between server authors and host clients.

## Learning Goals

- model required fields (`manifest_version`, `name`, `version`, `author`, `server`)
- use optional metadata for discoverability, support, and governance
- define compatibility constraints for clients, platforms, and runtimes
- avoid manifest drift that breaks host installation flows

## Manifest Priority Areas

| Area | Typical Fields |
|:-----|:---------------|
| identity | name, display name, version, description |
| compatibility | platform/runtime constraints, client versions |
| governance | license, repository, support, privacy policies |
| UX | icons, screenshots, localization resources |

## Source References

- [MCPB Manifest Spec](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md)

## Summary

You now have a manifest-first strategy for bundle interoperability and lifecycle management.

Next: [Chapter 3: Server Configuration and Runtime Packaging](03-server-configuration-and-runtime-packaging.md)
