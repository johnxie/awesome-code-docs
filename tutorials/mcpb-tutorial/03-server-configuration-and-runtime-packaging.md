---
layout: default
title: "Chapter 3: Server Configuration and Runtime Packaging"
nav_order: 3
parent: MCPB Tutorial
---

# Chapter 3: Server Configuration and Runtime Packaging

This chapter maps bundle runtime configuration to language-specific packaging realities.

## Learning Goals

- configure `server` and `mcp_config` fields correctly
- choose between Node, Python, Binary, and UV runtime paths
- understand dependency bundling tradeoffs by runtime type
- reduce install/runtime failures across host environments

## Runtime Strategy Matrix

| Server Type | Practical Guidance |
|:------------|:-------------------|
| node | easiest cross-platform baseline for many hosts |
| python | requires careful dependency/runtime packaging |
| binary | strongest portability if statically linked |
| uv | experimental path with host-managed Python/deps |

## Source References

- [MCPB README - Directory Structures](https://github.com/modelcontextprotocol/mcpb/blob/main/README.md#directory-structures)
- [Manifest Spec - Server Configuration](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md#server-configuration)
- [Hello World UV Example](https://github.com/modelcontextprotocol/mcpb/blob/main/examples/hello-world-uv/README.md)

## Summary

You now have a runtime packaging model for reliable MCPB installation and execution.

Next: [Chapter 4: Tools, Prompts, User Config, and Localization](04-tools-prompts-user-config-and-localization.md)
