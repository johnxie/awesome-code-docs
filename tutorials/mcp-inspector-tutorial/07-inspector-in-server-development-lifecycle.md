---
layout: default
title: "Chapter 7: Inspector in Server Development Lifecycle"
nav_order: 7
parent: MCP Inspector Tutorial
---


# Chapter 7: Inspector in Server Development Lifecycle

Welcome to **Chapter 7: Inspector in Server Development Lifecycle**. In this part of **MCP Inspector Tutorial: Debugging and Validating MCP Servers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Inspector is most effective when it is built into the normal MCP server development loop instead of used only for ad hoc debugging.

## Learning Goals

- position Inspector checks between local dev and release gates
- share reusable config profiles across team members
- validate server behavior after dependency and transport changes
- reduce drift between local runs and client-host configurations

## Lifecycle Pattern

1. implement server change
2. validate interactively in Inspector UI
3. export/update `mcp.json` entry
4. run CLI smoke checks in CI
5. publish with confidence once both loops pass

## Team Workflow Tips

- keep one minimal and one full-featured server config profile
- pin representative test tools/resources for regressions
- document expected failure modes (auth, timeout, transport)

## Source References

- [Inspector README - Config File Support](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#configuration)
- [Inspector README - Default Server Selection](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#default-server-selection)
- [Inspector Development Guide (AGENTS)](https://github.com/modelcontextprotocol/inspector/blob/main/AGENTS.md)

## Summary

You now have an integration model for using Inspector as a consistent part of server development.

Next: [Chapter 8: Production Ops, Testing, and Contribution](08-production-ops-testing-and-contribution.md)

## Source Code Walkthrough

### `cli/src/cli.ts`

The `runCli` function in [`cli/src/cli.ts`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/cli/src/cli.ts) handles a key part of this chapter's functionality:

```ts
}

async function runCli(args: Args): Promise<void> {
  const projectRoot = resolve(__dirname, "..");
  const cliPath = resolve(projectRoot, "build", "index.js");

  const abort = new AbortController();

  let cancelled = false;

  process.on("SIGINT", () => {
    cancelled = true;
    abort.abort();
  });

  try {
    // Build CLI arguments
    const cliArgs = [cliPath];

    // Add target URL/command first
    cliArgs.push(args.command, ...args.args);

    // Add transport flag if specified
    if (args.transport && args.transport !== "stdio") {
      // Convert streamable-http back to http for CLI mode
      const cliTransport =
        args.transport === "streamable-http" ? "http" : args.transport;
      cliArgs.push("--transport", cliTransport);
    }

    // Add headers if specified
    if (args.headers) {
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.

### `cli/src/cli.ts`

The `loadConfigFile` function in [`cli/src/cli.ts`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/cli/src/cli.ts) handles a key part of this chapter's functionality:

```ts
}

function loadConfigFile(configPath: string, serverName: string): ServerConfig {
  try {
    const resolvedConfigPath = path.isAbsolute(configPath)
      ? configPath
      : path.resolve(process.cwd(), configPath);

    if (!fs.existsSync(resolvedConfigPath)) {
      throw new Error(`Config file not found: ${resolvedConfigPath}`);
    }

    const configContent = fs.readFileSync(resolvedConfigPath, "utf8");
    const parsedConfig = JSON.parse(configContent);

    if (!parsedConfig.mcpServers || !parsedConfig.mcpServers[serverName]) {
      const availableServers = Object.keys(parsedConfig.mcpServers || {}).join(
        ", ",
      );
      throw new Error(
        `Server '${serverName}' not found in config file. Available servers: ${availableServers}`,
      );
    }

    const serverConfig = parsedConfig.mcpServers[serverName];

    return serverConfig;
  } catch (err: unknown) {
    if (err instanceof SyntaxError) {
      throw new Error(`Invalid JSON in config file: ${err.message}`);
    }

```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.

### `cli/src/cli.ts`

The `parseKeyValuePair` function in [`cli/src/cli.ts`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/cli/src/cli.ts) handles a key part of this chapter's functionality:

```ts
}

function parseKeyValuePair(
  value: string,
  previous: Record<string, string> = {},
): Record<string, string> {
  const parts = value.split("=");
  const key = parts[0];
  const val = parts.slice(1).join("=");

  if (val === undefined || val === "") {
    throw new Error(
      `Invalid parameter format: ${value}. Use key=value format.`,
    );
  }

  return { ...previous, [key as string]: val };
}

function parseHeaderPair(
  value: string,
  previous: Record<string, string> = {},
): Record<string, string> {
  const colonIndex = value.indexOf(":");

  if (colonIndex === -1) {
    throw new Error(
      `Invalid header format: ${value}. Use "HeaderName: Value" format.`,
    );
  }

  const key = value.slice(0, colonIndex).trim();
```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[runCli]
    B[loadConfigFile]
    C[parseKeyValuePair]
    A --> B
    B --> C
```
