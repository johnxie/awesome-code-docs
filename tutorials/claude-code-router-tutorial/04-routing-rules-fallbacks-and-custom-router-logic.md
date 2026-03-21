---
layout: default
title: "Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic"
nav_order: 4
parent: Claude Code Router Tutorial
---


# Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic

Welcome to **Chapter 4: Routing Rules, Fallbacks, and Custom Router Logic**. In this part of **Claude Code Router Tutorial: Multi-Provider Routing and Control Plane for Claude Code**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers how to shape model routing behavior by scenario and failure mode.

## Learning Goals

- configure scenario-based routes (`background`, `think`, `longContext`, etc.)
- apply fallback chains for resilience
- use project-level and custom router overrides responsibly
- route subagent workloads to explicit models where needed

## Routing Layers

1. global `Router.default` baseline
2. scenario-specific route overrides
3. project-level route files
4. optional custom router function
5. fallback model chains on failure

## Source References

- [Routing Config Docs](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/server/config/routing.md)
- [README: Router and Custom Router](https://github.com/musistudio/claude-code-router/blob/main/README.md#router)
- [README: Subagent Routing](https://github.com/musistudio/claude-code-router/blob/main/README.md#subagent-routing)

## Summary

You now know how to build robust routing logic with graceful degradation paths.

Next: [Chapter 5: CLI Operations: Model, Preset, and Statusline Workflows](05-cli-operations-model-preset-and-statusline-workflows.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `package.json`

The `package` module in [`package.json`](https://github.com/musistudio/claude-code-router/blob/HEAD/package.json) handles a key part of this chapter's functionality:

```json
{
  "name": "@musistudio/claude-code-router",
  "version": "2.0.0",
  "description": "Use Claude Code without an Anthropics account and route it to another LLM provider",
  "scripts": {
    "build": "pnpm build:shared && pnpm build:core && pnpm build:server && pnpm build:cli && pnpm build:ui",
    "build:core": "pnpm --filter @musistudio/llms build",
    "build:shared": "pnpm --filter @CCR/shared build",
    "build:cli": "pnpm --filter @CCR/cli build",
    "build:server": "pnpm --filter @CCR/server build",
    "build:ui": "pnpm --filter @CCR/ui build",
    "build:docs": "pnpm --filter claude-code-router-docs build",
    "release": "pnpm build && bash scripts/release.sh all",
    "release:npm": "bash scripts/release.sh npm",
    "release:docker": "bash scripts/release.sh docker",
    "dev:cli": "pnpm --filter @CCR/cli dev",
    "dev:server": "pnpm --filter @CCR/server dev",
    "dev:ui": "pnpm --filter @CCR/ui dev",
    "dev:core": "pnpm --filter @musistudio/llms dev",
    "dev:docs": "pnpm --filter claude-code-router-docs start",
    "serve:docs": "pnpm --filter claude-code-router-docs serve"
  },
  "bin": {
    "ccr": "dist/cli.js"
  },
  "keywords": [
    "claude",
    "code",
    "router",
    "llm",
    "anthropic"
  ],
  "author": "musistudio",
  "license": "MIT",
  "devDependencies": {
```

This module is important because it defines how Claude Code Router Tutorial: Multi-Provider Routing and Control Plane for Claude Code implements the patterns covered in this chapter.

### `examples/preset-manifest-example.json`

The `preset-manifest-example` module in [`examples/preset-manifest-example.json`](https://github.com/musistudio/claude-code-router/blob/HEAD/examples/preset-manifest-example.json) handles a key part of this chapter's functionality:

```json
{
  "name": "multi-provider-example",
  "version": "1.0.0",
  "description": "多Provider配置示例 - 支持OpenAI和DeepSeek切换",
  "author": "CCR Team",
  "keywords": ["openai", "deepseek", "multi-provider"],
  "ccrVersion": "2.0.0",
  "Providers": [
    {
      "name": "openai",
      "api_base_url": "https://api.openai.com/v1",
      "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
    },
    {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com",
      "models": ["deepseek-v3", "deepseek-chat"]
    }
  ],
  "schema": [
    {
      "id": "primaryProvider",
      "type": "select",
      "label": "主要Provider",
      "prompt": "选择您主要使用的LLM提供商",
      "options": {
        "type": "providers"
      },
      "required": true,
      "defaultValue": "openai"
    },
    {
      "id": "apiKey",
      "type": "password",
      "label": "API Key",
```

This module is important because it defines how Claude Code Router Tutorial: Multi-Provider Routing and Control Plane for Claude Code implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[package]
    B[preset-manifest-example]
    A --> B
```
