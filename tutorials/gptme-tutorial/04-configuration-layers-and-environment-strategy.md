---
layout: default
title: "Chapter 4: Configuration Layers and Environment Strategy"
nav_order: 4
parent: gptme Tutorial
---

# Chapter 4: Configuration Layers and Environment Strategy

gptme uses layered configuration across global, project, and chat scopes, with environment variables taking precedence.

## Config Layers

| Layer | Typical File |
|:------|:-------------|
| global | `~/.config/gptme/config.toml` |
| project | `gptme.toml` |
| per-chat | chat log `config.toml` |
| local overrides | `config.local.toml`, `gptme.local.toml` |

## Environment Policy

Use env vars for secrets and per-environment overrides; keep reusable behavior in versioned config files.

## Source References

- [gptme config docs](https://github.com/gptme/gptme/blob/master/docs/config.rst)

## Summary

You now have a deterministic strategy for managing gptme configuration across environments.

Next: [Chapter 5: Context, Lessons, and Conversation Management](05-context-lessons-and-conversation-management.md)
