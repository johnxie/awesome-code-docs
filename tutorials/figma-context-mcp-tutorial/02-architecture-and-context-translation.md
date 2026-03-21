---
layout: default
title: "Chapter 2: Architecture and Context Translation"
nav_order: 2
parent: Figma Context MCP Tutorial
---


# Chapter 2: Architecture and Context Translation

Welcome to **Chapter 2: Architecture and Context Translation**. In this part of **Figma Context MCP Tutorial: Design-to-Code Workflows for Coding Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


The server's core value is context translation: raw Figma API responses are simplified before being sent to the model.

## Translation Pipeline

```mermaid
flowchart LR
    A[Figma API Data] --> B[Context Simplification]
    B --> C[Relevant Layout and Style Payload]
    C --> D[Agent Prompt Context]
```

## Why Simplification Matters

- reduces irrelevant payload noise
- lowers token usage
- improves design fidelity in generated code

## Source References

- [Figma Context MCP README](https://github.com/GLips/Figma-Context-MCP)

## Summary

You now understand the transformation layer that makes MCP design context effective for coding agents.

Next: [Chapter 3: Frame Targeting and Context Scope](03-frame-targeting-and-context-scope.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `src/config.ts`

The `envStr` function in [`src/config.ts`](https://github.com/GLips/Figma-Context-MCP/blob/HEAD/src/config.ts) handles a key part of this chapter's functionality:

```ts
}

function envStr(name: string): string | undefined {
  return process.env[name] || undefined;
}

function envInt(...names: string[]): number | undefined {
  for (const name of names) {
    const val = process.env[name];
    if (val) return parseInt(val, 10);
  }
  return undefined;
}

function envBool(name: string): boolean | undefined {
  const val = process.env[name];
  if (val === "true") return true;
  if (val === "false") return false;
  return undefined;
}

function maskApiKey(key: string): string {
  if (!key || key.length <= 4) return "****";
  return `****${key.slice(-4)}`;
}

export function getServerConfig(): ServerConfig {
  const argv = cli({
    name: "figma-developer-mcp",
    version: process.env.NPM_PACKAGE_VERSION ?? "unknown",
    flags: {
      figmaApiKey: {
```

This function is important because it defines how Figma Context MCP Tutorial: Design-to-Code Workflows for Coding Agents implements the patterns covered in this chapter.

### `src/config.ts`

The `envInt` function in [`src/config.ts`](https://github.com/GLips/Figma-Context-MCP/blob/HEAD/src/config.ts) handles a key part of this chapter's functionality:

```ts
}

function envInt(...names: string[]): number | undefined {
  for (const name of names) {
    const val = process.env[name];
    if (val) return parseInt(val, 10);
  }
  return undefined;
}

function envBool(name: string): boolean | undefined {
  const val = process.env[name];
  if (val === "true") return true;
  if (val === "false") return false;
  return undefined;
}

function maskApiKey(key: string): string {
  if (!key || key.length <= 4) return "****";
  return `****${key.slice(-4)}`;
}

export function getServerConfig(): ServerConfig {
  const argv = cli({
    name: "figma-developer-mcp",
    version: process.env.NPM_PACKAGE_VERSION ?? "unknown",
    flags: {
      figmaApiKey: {
        type: String,
        description: "Figma API key (Personal Access Token)",
      },
      figmaOauthToken: {
```

This function is important because it defines how Figma Context MCP Tutorial: Design-to-Code Workflows for Coding Agents implements the patterns covered in this chapter.

### `src/config.ts`

The `envBool` function in [`src/config.ts`](https://github.com/GLips/Figma-Context-MCP/blob/HEAD/src/config.ts) handles a key part of this chapter's functionality:

```ts
}

function envBool(name: string): boolean | undefined {
  const val = process.env[name];
  if (val === "true") return true;
  if (val === "false") return false;
  return undefined;
}

function maskApiKey(key: string): string {
  if (!key || key.length <= 4) return "****";
  return `****${key.slice(-4)}`;
}

export function getServerConfig(): ServerConfig {
  const argv = cli({
    name: "figma-developer-mcp",
    version: process.env.NPM_PACKAGE_VERSION ?? "unknown",
    flags: {
      figmaApiKey: {
        type: String,
        description: "Figma API key (Personal Access Token)",
      },
      figmaOauthToken: {
        type: String,
        description: "Figma OAuth Bearer token",
      },
      env: {
        type: String,
        description: "Path to custom .env file to load environment variables from",
      },
      port: {
```

This function is important because it defines how Figma Context MCP Tutorial: Design-to-Code Workflows for Coding Agents implements the patterns covered in this chapter.

### `src/config.ts`

The `maskApiKey` function in [`src/config.ts`](https://github.com/GLips/Figma-Context-MCP/blob/HEAD/src/config.ts) handles a key part of this chapter's functionality:

```ts
}

function maskApiKey(key: string): string {
  if (!key || key.length <= 4) return "****";
  return `****${key.slice(-4)}`;
}

export function getServerConfig(): ServerConfig {
  const argv = cli({
    name: "figma-developer-mcp",
    version: process.env.NPM_PACKAGE_VERSION ?? "unknown",
    flags: {
      figmaApiKey: {
        type: String,
        description: "Figma API key (Personal Access Token)",
      },
      figmaOauthToken: {
        type: String,
        description: "Figma OAuth Bearer token",
      },
      env: {
        type: String,
        description: "Path to custom .env file to load environment variables from",
      },
      port: {
        type: Number,
        description: "Port to run the server on",
      },
      host: {
        type: String,
        description: "Host to run the server on",
      },
```

This function is important because it defines how Figma Context MCP Tutorial: Design-to-Code Workflows for Coding Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[envStr]
    B[envInt]
    C[envBool]
    D[maskApiKey]
    E[getServerConfig]
    A --> B
    B --> C
    C --> D
    D --> E
```
