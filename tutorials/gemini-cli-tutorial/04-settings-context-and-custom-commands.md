---
layout: default
title: "Chapter 4: Settings, Context, and Custom Commands"
nav_order: 4
parent: Gemini CLI Tutorial
---

# Chapter 4: Settings, Context, and Custom Commands

This chapter focuses on the highest-leverage configuration surfaces for consistent team behavior.

## Learning Goals

- manage runtime configuration through settings and CLI controls
- use context files effectively for persistent project guidance
- create reusable custom slash commands
- avoid configuration drift across user and workspace scopes

## Configuration Surfaces

- `~/.gemini/settings.json` for user-level defaults
- workspace `.gemini/settings.json` for project-local controls
- `GEMINI.md` for persistent context and operating rules

## Custom Command Pattern

Gemini CLI supports TOML-defined custom commands that can live in user or workspace scopes.

Benefits:

- reusable operation runbooks
- standardized prompt injection patterns
- better team consistency in frequent workflows

## Operational Checklist

- keep shared command namespaced by function
- version-control workspace command definitions
- review settings precedence when debugging behavior

## Source References

- [Settings Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/settings.md)
- [Context Files (GEMINI.md)](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md)
- [Custom Commands Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md)

## Summary

You now know how to codify Gemini CLI behavior with durable settings and commands.

Next: [Chapter 5: MCP, Extensions, and Skills](05-mcp-extensions-and-skills.md)
