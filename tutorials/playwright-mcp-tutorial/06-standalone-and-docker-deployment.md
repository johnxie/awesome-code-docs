---
layout: default
title: "Chapter 6: Standalone and Docker Deployment"
nav_order: 6
parent: Playwright MCP Tutorial
---


# Chapter 6: Standalone and Docker Deployment

Welcome to **Chapter 6: Standalone and Docker Deployment**. In this part of **Playwright MCP Tutorial: Browser Automation for Coding Agents Through MCP**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers deployment modes beyond basic stdio invocation.

## Learning Goals

- run Playwright MCP as a standalone HTTP MCP endpoint
- use Docker mode for cleaner host/runtime boundaries
- understand headless constraints in containerized mode
- connect clients to stable local MCP endpoints

## Deployment Patterns

| Pattern | Example | Best For |
|:--------|:--------|:---------|
| standalone local server | `npx @playwright/mcp@latest --port 8931` | multi-client local development |
| Docker hosted server | `mcr.microsoft.com/playwright/mcp` | cleaner runtime isolation |
| local stdio | default `npx` mode | simplest host integrations |

## Source References

- [README: Standalone MCP Server](https://github.com/microsoft/playwright-mcp/blob/main/README.md#standalone-mcp-server)
- [README: Docker Configuration](https://github.com/microsoft/playwright-mcp/blob/main/README.md#docker)
- [Dockerfile](https://github.com/microsoft/playwright-mcp/blob/main/Dockerfile)

## Summary

You now have options for scaling Playwright MCP beyond default client-managed execution.

Next: [Chapter 7: Tooling Surface and Automation Patterns](07-tooling-surface-and-automation-patterns.md)

## Source Code Walkthrough

### `roll.js`

The `doRoll` function in [`roll.js`](https://github.com/microsoft/playwright-mcp/blob/HEAD/roll.js) handles a key part of this chapter's functionality:

```js
}

function doRoll(version) {
  updatePlaywrightVersion(version);
  copyConfig();
  // update readme
  execSync('npm run lint', { cwd: __dirname, stdio: 'inherit' });
}

let version = process.argv[2];
if (!version) {
  version = execSync('npm info playwright@next version', { encoding: 'utf-8' }).trim();
  console.log(`Using next playwright version: ${version}`);
}
doRoll(version);

```

This function is important because it defines how Playwright MCP Tutorial: Browser Automation for Coding Agents Through MCP implements the patterns covered in this chapter.

### `packages/playwright-mcp/index.d.ts`

The `createConnection` function in [`packages/playwright-mcp/index.d.ts`](https://github.com/microsoft/playwright-mcp/blob/HEAD/packages/playwright-mcp/index.d.ts) handles a key part of this chapter's functionality:

```ts
import type { BrowserContext } from 'playwright';

export declare function createConnection(config?: Config, contextGetter?: () => Promise<BrowserContext>): Promise<Server>;
export {};

```

This function is important because it defines how Playwright MCP Tutorial: Browser Automation for Coding Agents Through MCP implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[doRoll]
    B[createConnection]
    A --> B
```
