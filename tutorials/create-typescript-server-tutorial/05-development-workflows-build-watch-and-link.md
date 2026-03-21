---
layout: default
title: "Chapter 5: Development Workflows: Build, Watch, and Link"
nav_order: 5
parent: Create TypeScript Server Tutorial
---


# Chapter 5: Development Workflows: Build, Watch, and Link

Welcome to **Chapter 5: Development Workflows: Build, Watch, and Link**. In this part of **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers practical day-to-day development loops.

## Learning Goals

- use build/watch modes for rapid iteration
- link local binaries for integration testing
- structure scripts and environment setup for team consistency
- reduce iteration friction across development environments

## Core Workflow

1. `npm run build` for one-shot compile
2. `npm run watch` for iterative development
3. `npm link` when local command exposure is useful

## Source References

- [Create TypeScript Server README](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/README.md)
- [Template README - Development](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/README.md.ejs#development)

## Summary

You now have a repeatable development loop for generated server projects.

Next: [Chapter 6: Debugging and Local Integration](06-debugging-and-local-integration.md)

## Source Code Walkthrough

### `src/index.ts`

The `index` module in [`src/index.ts`](https://github.com/modelcontextprotocol/create-typescript-server/blob/HEAD/src/index.ts) handles a key part of this chapter's functionality:

```ts
#!/usr/bin/env node
import chalk from "chalk";
import { Command } from "commander";
import ejs from "ejs";
import fs from "fs/promises";
import inquirer from "inquirer";
import ora from "ora";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
function getClaudeConfigDir(): string {
  switch (os.platform()) {
    case "darwin":
      return path.join(
        os.homedir(),
        "Library",
        "Application Support",
        "Claude",
      );
    case "win32":
      if (!process.env.APPDATA) {
        throw new Error("APPDATA environment variable is not set");
      }
      return path.join(process.env.APPDATA, "Claude");
    default:
      throw new Error(
        `Unsupported operating system for Claude configuration: ${os.platform()}`,
      );
  }
}

async function updateClaudeConfig(name: string, directory: string) {
  try {
```

This module is important because it defines how Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates implements the patterns covered in this chapter.

### `tsconfig.json`

The `tsconfig` module in [`tsconfig.json`](https://github.com/modelcontextprotocol/create-typescript-server/blob/HEAD/tsconfig.json) handles a key part of this chapter's functionality:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "**/*.spec.ts"]
}

```

This module is important because it defines how Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates implements the patterns covered in this chapter.

### `package.json`

The `package` module in [`package.json`](https://github.com/modelcontextprotocol/create-typescript-server/blob/HEAD/package.json) handles a key part of this chapter's functionality:

```json
{
  "name": "@modelcontextprotocol/create-server",
  "version": "0.3.1",
  "description": "CLI tool to create new MCP servers",
  "license": "MIT",
  "author": "Anthropic, PBC (https://anthropic.com)",
  "homepage": "https://modelcontextprotocol.io",
  "bugs": "https://github.com/modelcontextprotocol/create-typescript-server/issues",
  "type": "module",
  "bin": {
    "create-mcp-server": "build/index.js"
  },
  "files": [
    "build",
    "template"
  ],
  "scripts": {
    "build": "tsc && shx chmod +x build/index.js",
    "prepare": "npm run build",
    "watch": "tsc --watch"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "0.6.0",
    "chalk": "^5.3.0",
    "commander": "^12.0.0",
    "ejs": "^3.1.9",
    "inquirer": "^9.2.15",
    "ora": "^8.0.1"
  },
  "devDependencies": {
    "@types/ejs": "^3.1.5",
    "@types/inquirer": "^9.0.7",
    "@types/node": "^20.11.24",
    "shx": "^0.3.4",
    "typescript": "^5.3.3"
```

This module is important because it defines how Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[index]
    B[tsconfig]
    C[package]
    A --> B
    B --> C
```
