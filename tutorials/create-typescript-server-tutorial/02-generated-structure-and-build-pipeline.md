---
layout: default
title: "Chapter 2: Generated Structure and Build Pipeline"
nav_order: 2
parent: Create TypeScript Server Tutorial
---


# Chapter 2: Generated Structure and Build Pipeline

Welcome to **Chapter 2: Generated Structure and Build Pipeline**. In this part of **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains scaffold output and build toolchain expectations.

## Learning Goals

- navigate generated source/template file structure
- understand TypeScript compile and watch workflows
- map scaffold defaults to publishable package outputs
- avoid common build misconfiguration issues

## Source References

- [Template README](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/README.md.ejs)
- [Template TypeScript Config](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/tsconfig.json)

## Summary

You now have structural and build-level orientation for generated projects.

Next: [Chapter 3: Template MCP Primitives: Resources, Tools, Prompts](03-template-mcp-primitives-resources-tools-prompts.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `src/index.ts`

The `updateClaudeConfig` function in [`src/index.ts`](https://github.com/modelcontextprotocol/create-typescript-server/blob/HEAD/src/index.ts) handles a key part of this chapter's functionality:

```ts
}

async function updateClaudeConfig(name: string, directory: string) {
  try {
    const configFile = path.join(
      getClaudeConfigDir(),
      "claude_desktop_config.json",
    );

    let config;
    try {
      config = JSON.parse(await fs.readFile(configFile, "utf-8"));
    } catch (err) {
      if ((err as NodeJS.ErrnoException).code !== "ENOENT") {
        throw err;
      }

      // File doesn't exist, create initial config
      config = {};
      await fs.mkdir(path.dirname(configFile), { recursive: true });
    }

    if (!config.mcpServers) {
      config.mcpServers = {};
    }

    if (config.mcpServers[name]) {
      const { replace } = await inquirer.prompt([
        {
          type: "confirm",
          name: "replace",
          message: `An MCP server named "${name}" is already configured for Claude.app. Do you want to replace it?`,
```

This function is important because it defines how Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[updateClaudeConfig]
```
