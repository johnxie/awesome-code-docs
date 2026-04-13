---
layout: default
title: "Chapter 4: CLI Mode, Automation, and CI Loops"
nav_order: 4
parent: MCP Inspector Tutorial
---


# Chapter 4: CLI Mode, Automation, and CI Loops

Welcome to **Chapter 4: CLI Mode, Automation, and CI Loops**. In this part of **MCP Inspector Tutorial: Debugging and Validating MCP Servers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Inspector CLI mode is the bridge from manual debugging to deterministic automation.

## Learning Goals

- run CLI mode against local and remote MCP servers
- script list/call flows for smoke tests
- pass headers and args safely for CI use
- standardize JSON outputs for pipeline checks

## Core CLI Patterns

```bash
# Local stdio server, list tools
npx @modelcontextprotocol/inspector --cli node build/index.js --method tools/list

# Call a tool with arguments
npx @modelcontextprotocol/inspector --cli node build/index.js \
  --method tools/call --tool-name mytool --tool-arg key=value

# Remote streamable HTTP endpoint
npx @modelcontextprotocol/inspector --cli https://example.com/mcp \
  --transport http --method resources/list
```

## CI Strategy

- keep one golden endpoint per server family for smoke checks
- run read-only calls first (`tools/list`, `resources/list`)
- treat timeouts and transport errors as separate failure classes
- persist raw JSON output for regression diffs

## Source References

- [Inspector README - CLI Mode](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#cli-mode)
- [Inspector CLI Package](https://github.com/modelcontextprotocol/inspector/tree/main/cli)

## Summary

You can now automate Inspector-based checks in build and release pipelines.

Next: [Chapter 5: Security, Auth, and Network Hardening](05-security-auth-and-network-hardening.md)

## Source Code Walkthrough

### `client/bin/start.js`

The `getClientUrl` function in [`client/bin/start.js`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/client/bin/start.js) handles a key part of this chapter's functionality:

```js
}

function getClientUrl(port, authDisabled, sessionToken, serverPort) {
  const host = process.env.HOST || "localhost";
  const baseUrl = `http://${host}:${port}`;

  const params = new URLSearchParams();
  if (serverPort && serverPort !== DEFAULT_MCP_PROXY_LISTEN_PORT) {
    params.set("MCP_PROXY_PORT", serverPort);
  }
  if (!authDisabled) {
    params.set("MCP_PROXY_AUTH_TOKEN", sessionToken);
  }
  return params.size > 0 ? `${baseUrl}/?${params.toString()}` : baseUrl;
}

async function startDevServer(serverOptions) {
  const {
    SERVER_PORT,
    CLIENT_PORT,
    sessionToken,
    envVars,
    abort,
    transport,
    serverUrl,
  } = serverOptions;
  const serverCommand = "npx";
  const serverArgs = ["tsx", "watch", "--clear-screen=false", "src/index.ts"];
  const isWindows = process.platform === "win32";

  const spawnOptions = {
    cwd: resolve(__dirname, "../..", "server"),
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.

### `client/bin/start.js`

The `startDevServer` function in [`client/bin/start.js`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/client/bin/start.js) handles a key part of this chapter's functionality:

```js
}

async function startDevServer(serverOptions) {
  const {
    SERVER_PORT,
    CLIENT_PORT,
    sessionToken,
    envVars,
    abort,
    transport,
    serverUrl,
  } = serverOptions;
  const serverCommand = "npx";
  const serverArgs = ["tsx", "watch", "--clear-screen=false", "src/index.ts"];
  const isWindows = process.platform === "win32";

  const spawnOptions = {
    cwd: resolve(__dirname, "../..", "server"),
    env: {
      ...process.env,
      SERVER_PORT,
      CLIENT_PORT,
      MCP_PROXY_AUTH_TOKEN: sessionToken,
      MCP_ENV_VARS: JSON.stringify(envVars),
      ...(transport ? { MCP_TRANSPORT: transport } : {}),
      ...(serverUrl ? { MCP_SERVER_URL: serverUrl } : {}),
    },
    signal: abort.signal,
    echoOutput: true,
  };

  // For Windows, we need to ignore stdin to simulate < NUL
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.

### `client/bin/start.js`

The `startProdServer` function in [`client/bin/start.js`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/client/bin/start.js) handles a key part of this chapter's functionality:

```js
}

async function startProdServer(serverOptions) {
  const {
    SERVER_PORT,
    CLIENT_PORT,
    sessionToken,
    envVars,
    abort,
    command,
    mcpServerArgs,
    transport,
    serverUrl,
  } = serverOptions;
  const inspectorServerPath = resolve(
    __dirname,
    "../..",
    "server",
    "build",
    "index.js",
  );

  const server = spawnPromise(
    "node",
    [
      inspectorServerPath,
      ...(command ? [`--command=${command}`] : []),
      ...(mcpServerArgs && mcpServerArgs.length > 0
        ? [`--args=${mcpServerArgs.join(" ")}`]
        : []),
      ...(transport ? [`--transport=${transport}`] : []),
      ...(serverUrl ? [`--server-url=${serverUrl}`] : []),
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[getClientUrl]
    B[startDevServer]
    C[startProdServer]
    A --> B
    B --> C
```
