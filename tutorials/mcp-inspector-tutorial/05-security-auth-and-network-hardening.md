---
layout: default
title: "Chapter 5: Security, Auth, and Network Hardening"
nav_order: 5
parent: MCP Inspector Tutorial
---


# Chapter 5: Security, Auth, and Network Hardening

Welcome to **Chapter 5: Security, Auth, and Network Hardening**. In this part of **MCP Inspector Tutorial: Debugging and Validating MCP Servers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Inspector's proxy can spawn local processes and connect to arbitrary endpoints, so hardening defaults matters.

## Learning Goals

- keep authentication enabled and token scope tight
- use local-only binding as a default posture
- configure allowed origins for DNS rebinding defense
- understand risks of disabling auth

## Hardening Checklist

| Control | Recommended Setting | Why |
|:--------|:--------------------|:----|
| Proxy auth | enabled | blocks unauthorized requests to process-spawning proxy |
| Binding | localhost only | reduces LAN exposure |
| Origins | explicit allowlist | protects against DNS rebinding attacks |
| `DANGEROUSLY_OMIT_AUTH` | never in routine dev | large local compromise risk |

## High-Risk Anti-Pattern

Avoid using `DANGEROUSLY_OMIT_AUTH=true` unless you are in a tightly isolated throwaway environment with a clear security reason.

## Source References

- [Inspector README - Security Considerations](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#security-considerations)
- [Inspector README - Local-only Binding](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#local-only-binding)
- [Inspector README - DNS Rebinding Protection](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#dns-rebinding-protection)

## Summary

You now have a concrete baseline for safer Inspector operation.

Next: [Chapter 6: Configuration, Timeouts, and Runtime Tuning](06-configuration-timeouts-and-runtime-tuning.md)

## Source Code Walkthrough

### `client/bin/start.js`

The `startDevClient` function in [`client/bin/start.js`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/client/bin/start.js) handles a key part of this chapter's functionality:

```js
}

async function startDevClient(clientOptions) {
  const {
    CLIENT_PORT,
    SERVER_PORT,
    authDisabled,
    sessionToken,
    abort,
    cancelled,
  } = clientOptions;
  const clientCommand = "npx";
  const host = process.env.HOST || "localhost";
  const clientArgs = ["vite", "--port", CLIENT_PORT, "--host", host];
  const isWindows = process.platform === "win32";

  const spawnOptions = {
    cwd: resolve(__dirname, ".."),
    env: { ...process.env, CLIENT_PORT },
    signal: abort.signal,
    echoOutput: true,
  };

  // For Windows, we need to ignore stdin to prevent hanging
  if (isWindows) {
    spawnOptions.stdio = ["ignore", "pipe", "pipe"];
  }

  const client = spawn(clientCommand, clientArgs, spawnOptions);

  const url = getClientUrl(
    CLIENT_PORT,
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.

### `client/bin/start.js`

The `startProdClient` function in [`client/bin/start.js`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/client/bin/start.js) handles a key part of this chapter's functionality:

```js
}

async function startProdClient(clientOptions) {
  const {
    CLIENT_PORT,
    SERVER_PORT,
    authDisabled,
    sessionToken,
    abort,
    cancelled,
  } = clientOptions;
  const inspectorClientPath = resolve(
    __dirname,
    "../..",
    "client",
    "bin",
    "client.js",
  );

  const url = getClientUrl(
    CLIENT_PORT,
    authDisabled,
    sessionToken,
    SERVER_PORT,
  );

  await spawnPromise("node", [inspectorClientPath], {
    env: {
      ...process.env,
      CLIENT_PORT,
      INSPECTOR_URL: url,
    },
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.

### `client/bin/start.js`

The `main` function in [`client/bin/start.js`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/client/bin/start.js) handles a key part of this chapter's functionality:

```js
}

async function main() {
  // Parse command line arguments
  const args = process.argv.slice(2);
  const envVars = {};
  const mcpServerArgs = [];
  let command = null;
  let parsingFlags = true;
  let isDev = false;
  let transport = null;
  let serverUrl = null;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (parsingFlags && arg === "--") {
      parsingFlags = false;
      continue;
    }

    if (parsingFlags && arg === "--dev") {
      isDev = true;
      continue;
    }

    if (parsingFlags && arg === "--transport" && i + 1 < args.length) {
      transport = args[++i];
      continue;
    }

    if (parsingFlags && arg === "--server-url" && i + 1 < args.length) {
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[startDevClient]
    B[startProdClient]
    C[main]
    A --> B
    B --> C
```
