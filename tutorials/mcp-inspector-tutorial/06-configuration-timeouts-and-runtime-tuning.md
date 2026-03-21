---
layout: default
title: "Chapter 6: Configuration, Timeouts, and Runtime Tuning"
nav_order: 6
parent: MCP Inspector Tutorial
---


# Chapter 6: Configuration, Timeouts, and Runtime Tuning

Welcome to **Chapter 6: Configuration, Timeouts, and Runtime Tuning**. In this part of **MCP Inspector Tutorial: Debugging and Validating MCP Servers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


The default timeout behavior is good for quick tests, but long-running tools and interactive flows need explicit tuning.

## Learning Goals

- tune request timeout values for realistic workloads
- use progress-aware timeout reset behavior correctly
- separate client-side timeout policy from server-side limits
- manage profile-like configs for multiple targets

## Key Runtime Settings

| Setting | Purpose | Typical Adjustment |
|:--------|:--------|:-------------------|
| `MCP_SERVER_REQUEST_TIMEOUT` | client request timeout | increase for slow tool operations |
| `MCP_REQUEST_TIMEOUT_RESET_ON_PROGRESS` | extend timeout on progress events | keep enabled for streaming/progress tools |
| `MCP_REQUEST_MAX_TOTAL_TIMEOUT` | max total duration cap | set upper bound for long tasks |
| `MCP_PROXY_FULL_ADDRESS` | non-default proxy address | required for remote/devbox scenarios |
| `MCP_AUTO_OPEN_ENABLED` | browser auto-open behavior | disable in CI/headless contexts |

## Practical Rule

Set Inspector timeout ceilings high enough for legitimate long calls, but keep a finite max timeout to prevent invisible hangs.

## Source References

- [Inspector README - Configuration](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#configuration)
- [Inspector README - Note on Timeouts](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#configuration)

## Summary

You now have a runtime tuning approach that reduces false failures and stalled sessions.

Next: [Chapter 7: Inspector in Server Development Lifecycle](07-inspector-in-server-development-lifecycle.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `cli/src/cli.ts`

The `runWebClient` function in [`cli/src/cli.ts`](https://github.com/modelcontextprotocol/inspector/blob/HEAD/cli/src/cli.ts) handles a key part of this chapter's functionality:

```ts
}

async function runWebClient(args: Args): Promise<void> {
  // Path to the client entry point
  const inspectorClientPath = resolve(
    __dirname,
    "../../",
    "client",
    "bin",
    "start.js",
  );

  const abort = new AbortController();
  let cancelled: boolean = false;
  process.on("SIGINT", () => {
    cancelled = true;
    abort.abort();
  });

  // Build arguments to pass to start.js
  const startArgs: string[] = [];

  // Pass environment variables
  for (const [key, value] of Object.entries(args.envArgs)) {
    startArgs.push("-e", `${key}=${value}`);
  }

  // Pass transport type if specified
  if (args.transport) {
    startArgs.push("--transport", args.transport);
  }

```

This function is important because it defines how MCP Inspector Tutorial: Debugging and Validating MCP Servers implements the patterns covered in this chapter.

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


## How These Components Connect

```mermaid
flowchart TD
    A[runWebClient]
    B[runCli]
    C[loadConfigFile]
    A --> B
    B --> C
```
