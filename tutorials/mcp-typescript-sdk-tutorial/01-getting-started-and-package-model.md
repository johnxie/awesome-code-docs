---
layout: default
title: "Chapter 1: Getting Started and Package Model"
nav_order: 1
parent: MCP TypeScript SDK Tutorial
---

# Chapter 1: Getting Started and Package Model

The MCP TypeScript SDK v2 is a monorepo of split packages that replaces the single `@modelcontextprotocol/sdk` from v1. This chapter establishes the correct package baseline, explains which packages serve which roles, and gets your first client and server running.

## Learning Goals

- Distinguish v1 and v2 package structures before writing any code
- Choose the right packages for your use case (client-only, server-only, both)
- Run first server and client examples from the repository
- Avoid dependency drift around `zod` and Node.js versions

## The v2 Package Split

```mermaid
graph TD
    OLD[v1: @modelcontextprotocol/sdk\nMonolithic — everything in one package]

    NEW[v2: Split packages]
    NEW --> CORE[@modelcontextprotocol/core\nTypes, protocol, transport interfaces\nDo not import directly]
    NEW --> CLIENT[@modelcontextprotocol/client\nClient + StdioClientTransport\n+ StreamableHTTPClientTransport + SSE]
    NEW --> SERVER[@modelcontextprotocol/server\nMcpServer + StdioServerTransport\n+ WebStandardStreamableHTTPServerTransport]
    NEW --> NODE[@modelcontextprotocol/node\nNodeStreamableHTTPServerTransport\nfor Node.js native http module]
    NEW --> EXPRESS[@modelcontextprotocol/express\nExpress middleware + host validation]
    NEW --> HONO[@modelcontextprotocol/hono\nHono web-standard adapter]
```

`@modelcontextprotocol/core` is an internal package — import types from whichever of `client` or `server` you already depend on. They both re-export everything you need.

## Installation

```bash
# Client-only project
npm install @modelcontextprotocol/client

# Server-only project (stdio or web-standard HTTP)
npm install @modelcontextprotocol/server

# Server project using Node.js native http module
npm install @modelcontextprotocol/server @modelcontextprotocol/node

# Server with Express integration
npm install @modelcontextprotocol/server @modelcontextprotocol/express

# Full-stack (client + server in same project)
npm install @modelcontextprotocol/client @modelcontextprotocol/server
```

**No zod needed in most cases** — v2 dropped the `zod` peer dependency. You can still use zod in your own server code for input validation, but it is no longer required by the SDK itself.

## Runtime Requirements

| Requirement | v1 | v2 |
|:------------|:---|:---|
| Node.js | 18+ | **20+** |
| Module format | CJS + ESM | **ESM only** |
| TypeScript | 4.x+ | 5.x recommended |

If your project uses CommonJS (`require()`), you must either migrate to ESM or use dynamic `import()` calls.

## First Server (Minimal)

```typescript
// server.ts
import { McpServer } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server';

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

server.registerTool("hello", {
  description: "Say hello",
  inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] },
}, async ({ name }) => ({
  content: [{ type: "text", text: `Hello, ${name}!` }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

```bash
npx ts-node server.ts
# or after build:
node dist/server.js
```

## First Client (Minimal)

```typescript
// client.ts
import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client';

const client = new Client({ name: "my-client", version: "1.0.0" });
const transport = new StdioClientTransport({
  command: "node",
  args: ["dist/server.js"]
});

await client.connect(transport);

const tools = await client.listTools();
console.log("Tools:", tools.tools.map(t => t.name));

const result = await client.callTool({ name: "hello", arguments: { name: "World" } });
console.log("Result:", result.content[0].text);

await client.close();
```

## Package Dependency Diagram

```mermaid
graph LR
    YOUR_PROJECT[Your Project]
    YOUR_PROJECT --> CLIENT[@modelcontextprotocol/client]
    YOUR_PROJECT --> SERVER[@modelcontextprotocol/server]
    YOUR_PROJECT --> NODE[@modelcontextprotocol/node\noptional]
    YOUR_PROJECT --> EXPRESS[@modelcontextprotocol/express\noptional]

    CLIENT --> CORE[@modelcontextprotocol/core\nauto-installed]
    SERVER --> CORE
    NODE --> CORE
    EXPRESS --> NODE
```

All middleware packages depend on `core` transitively. You never need to add `core` to your own `package.json`.

## v1 Import Map

If you are migrating from v1, here is the import mapping:

| v1 import path | v2 import |
|:--------------|:----------|
| `@modelcontextprotocol/sdk/client/index.js` | `@modelcontextprotocol/client` |
| `@modelcontextprotocol/sdk/server/mcp.js` | `@modelcontextprotocol/server` |
| `@modelcontextprotocol/sdk/types.js` | `@modelcontextprotocol/client` or `server` |
| `@modelcontextprotocol/sdk/client/streamableHttp.js` | `@modelcontextprotocol/client` |
| `@modelcontextprotocol/sdk/server/streamableHttp.js` | `@modelcontextprotocol/node` (renamed to `NodeStreamableHTTPServerTransport`) |
| `@modelcontextprotocol/sdk/client/stdio.js` | `@modelcontextprotocol/client` |
| `@modelcontextprotocol/sdk/server/stdio.js` | `@modelcontextprotocol/server` |

## Source References

- [TypeScript SDK README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md)
- [Migration Guide (v1 → v2)](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/migration.md)
- [Client package README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/client/README.md)
- [Server package README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/server/README.md)
- [FAQ](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/faq.md)

## Summary

The v2 SDK splits the monolithic `@modelcontextprotocol/sdk` into focused packages: `client`, `server`, `node`, `express`, `hono`. Node.js 20+ and ESM are required. Zod is no longer a peer dependency. The `core` package is internal — import from `client` or `server` instead. For new projects, install only the packages your role requires.

Next: [Chapter 2: Server Transports and Deployment Patterns](02-server-transports-and-deployment-patterns.md)
