---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Context7 Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **Context7 Tutorial: Live Documentation Context for Coding Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gets Context7 connected to your coding agent so documentation lookups work immediately.

## Learning Goals

- choose local or remote Context7 MCP deployment
- connect Context7 in your primary coding client
- verify tool connectivity and first query
- avoid common first-install mistakes

## Fast Install Patterns

| Pattern | Example |
|:--------|:--------|
| Claude Code local | `claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY` |
| Claude Code remote | `claude mcp add --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp` |
| Cursor remote config | MCP URL `https://mcp.context7.com/mcp` + optional API key header |

## First-Use Checklist

1. add Context7 MCP server in your client
2. run client MCP status command or panel
3. ask a targeted library question with `use context7`
4. confirm the response cites current docs patterns

## Source References

- [Context7 README: Installation](https://github.com/upstash/context7/blob/master/README.md#installation)
- [Claude Code client guide](https://context7.com/docs/clients/claude-code)
- [Cursor client guide](https://context7.com/docs/clients/cursor)

## Summary

You now have Context7 running and reachable from your coding client.

Next: [Chapter 2: Architecture and Tooling Model](02-architecture-and-tooling-model.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `server.json`

The `server` module in [`server.json`](https://github.com/upstash/context7/blob/HEAD/server.json) handles a key part of this chapter's functionality:

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.upstash/context7",
  "title": "Context7",
  "description": "Up-to-date code docs for any prompt",
  "repository": {
    "url": "https://github.com/upstash/context7",
    "source": "github"
  },
  "websiteUrl": "https://context7.com",
  "icons": [
    {
      "src": "https://raw.githubusercontent.com/upstash/context7/master/public/icon.png",
      "mimeType": "image/png"
    }
  ],
  "version": "2.0.0",
  "packages": [
    {
      "registryType": "npm",
      "identifier": "@upstash/context7-mcp",
      "version": "2.0.2",
      "transport": {
        "type": "stdio"
      },
      "environmentVariables": [
        {
          "name": "CONTEXT7_API_KEY",
          "description": "API key for authentication",
          "isRequired": false,
          "isSecret": true
        }
      ]
    },
    {
```

This module is important because it defines how Context7 Tutorial: Live Documentation Context for Coding Agents implements the patterns covered in this chapter.

### `docs/docs.json`

The `docs` module in [`docs/docs.json`](https://github.com/upstash/context7/blob/HEAD/docs/docs.json) handles a key part of this chapter's functionality:

```json
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "Context7 MCP",
  "description": "Up-to-date code docs for any prompt.",
  "colors": {
    "primary": "#10B981",
    "light": "#ECFDF5",
    "dark": "#064E3B"
  },
  "contextual": {
    "options": [
      "copy",
      "view",
      "chatgpt",
      "claude"
    ]
  },
  "navigation": {
    "groups": [
      {
        "group": "Overview",
        "pages": [
          "overview",
          "installation",
          "plans-pricing",
          "clients/cli",
          "adding-libraries",
          "api-guide",
          "skills",
          "tips"
        ]
      },
      {
        "group": "How To",
```

This module is important because it defines how Context7 Tutorial: Live Documentation Context for Coding Agents implements the patterns covered in this chapter.

### `eslint.config.js`

The `eslint.config` module in [`eslint.config.js`](https://github.com/upstash/context7/blob/HEAD/eslint.config.js) handles a key part of this chapter's functionality:

```js
import tseslint from "typescript-eslint";
import eslintPluginPrettier from "eslint-plugin-prettier";

export default tseslint.config({
  // Base ESLint configuration
  ignores: ["node_modules/**", "build/**", "dist/**", ".git/**", ".github/**"],
  languageOptions: {
    ecmaVersion: 2020,
    sourceType: "module",
    parser: tseslint.parser,
    parserOptions: {},
    globals: {
      // Add Node.js globals
      process: "readonly",
      require: "readonly",
      module: "writable",
      console: "readonly",
    },
  },
  // Settings for all files
  linterOptions: {
    reportUnusedDisableDirectives: true,
  },
  // Apply ESLint recommended rules
  extends: [tseslint.configs.recommended],
  plugins: {
    prettier: eslintPluginPrettier,
  },
  rules: {
    // TypeScript rules
    "@typescript-eslint/explicit-module-boundary-types": "off",
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    "@typescript-eslint/no-explicit-any": "warn",
    // Prettier integration
    "prettier/prettier": "error",
```

This module is important because it defines how Context7 Tutorial: Live Documentation Context for Coding Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[server]
    B[docs]
    C[eslint.config]
    A --> B
    B --> C
```
