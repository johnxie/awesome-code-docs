---
layout: default
title: "Chapter 6: Middleware, Security, and Host Validation"
nav_order: 6
parent: MCP TypeScript SDK Tutorial
---


# Chapter 6: Middleware, Security, and Host Validation

Welcome to **Chapter 6: Middleware, Security, and Host Validation**. In this part of **MCP TypeScript SDK Tutorial: Building and Migrating MCP Clients and Servers in TypeScript**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Most server risk in local and internal environments comes from weak host/binding controls, not tool code.

## Learning Goals

- apply framework adapter defaults that reduce exposure
- configure host header validation and allowed hostnames
- align localhost development and network-access behavior safely
- separate runtime adapter concerns from protocol concerns

## Security Checklist

| Control | Recommendation |
|:--------|:---------------|
| Local host binding | default to localhost/loopback |
| Host validation | explicit allowlist when externally bound |
| Adapter choice | match runtime, keep adapters thin |
| Legacy SSE | keep only for compatibility windows |

## Source References

- [Server Docs - DNS rebinding protection](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/server.md)
- [Express Adapter README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/middleware/express/README.md)
- [Hono Adapter README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/packages/middleware/hono/README.md)

## Summary

You now have concrete controls for hardening local and remote server exposure.

Next: [Chapter 7: v1 to v2 Migration Strategy](07-v1-to-v2-migration-strategy.md)

## Source Code Walkthrough

### `scripts/sync-snippets.ts`

The `getOrLoadRegion` function in [`scripts/sync-snippets.ts`](https://github.com/modelcontextprotocol/typescript-sdk/blob/HEAD/scripts/sync-snippets.ts) handles a key part of this chapter's functionality:

```ts
 * @returns The extracted code string
 */
function getOrLoadRegion(
  sourceFilePath: string,
  examplePath: string,
  regionName: string | undefined,
  cache: RegionCache,
): string {
  // Resolve the example path relative to the source file
  const sourceDir = dirname(sourceFilePath);
  const absoluteExamplePath = resolve(sourceDir, examplePath);

  // File content is always cached with key ending in "#" (empty region)
  const fileKey = `${absoluteExamplePath}#`;
  let fileContent = cache.get(fileKey);

  if (fileContent === undefined) {
    try {
      fileContent = readFileSync(absoluteExamplePath, 'utf-8');
    } catch {
      throw new Error(`Example file not found: ${absoluteExamplePath}`);
    }
    cache.set(fileKey, fileContent);
  }

  // If no region name, return whole file
  if (!regionName) {
    return fileContent.trim();
  }

  // Extract region from cached file content, cache the result
  const regionKey = `${absoluteExamplePath}#${regionName}`;
```

This function is important because it defines how MCP TypeScript SDK Tutorial: Building and Migrating MCP Clients and Servers in TypeScript implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[getOrLoadRegion]
```
