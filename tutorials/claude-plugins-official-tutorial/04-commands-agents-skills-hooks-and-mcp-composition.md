---
layout: default
title: "Chapter 4: Commands, Agents, Skills, Hooks, and MCP Composition"
nav_order: 4
parent: Claude Plugins Official Tutorial
---

# Chapter 4: Commands, Agents, Skills, Hooks, and MCP Composition

This chapter explains how plugin capability types combine to form reliable workflows.

## Learning Goals

- understand distinct roles of commands, agents, skills, hooks, and MCP
- compose plugin capabilities without unnecessary complexity
- map capability choices to user-facing workflow outcomes
- avoid overloading single plugins with conflicting concerns

## Capability Composition Model

- commands: deterministic entrypoints
- agents: specialized reasoning personas
- skills: reusable domain instruction packs
- hooks: lifecycle automation and enforcement
- MCP: external tool/system integrations

## Practical Composition Pattern

- start with command-first workflow entrypoint
- add one or two specialist agents where reasoning depth is needed
- add skills for repeated domain knowledge patterns
- attach hooks only where automation policy is clear

## Source References

- [Example Plugin Capabilities](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/example-plugin)
- [Code Review Plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review)
- [Hookify Plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/hookify)

## Summary

You now know how to compose plugin capabilities into maintainable workflows.

Next: [Chapter 5: Trust, Security, and Risk Controls](05-trust-security-and-risk-controls.md)
