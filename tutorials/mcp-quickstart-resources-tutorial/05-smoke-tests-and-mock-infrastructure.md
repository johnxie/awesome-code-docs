---
layout: default
title: "Chapter 5: Smoke Tests and Mock Infrastructure"
nav_order: 5
parent: MCP Quickstart Resources Tutorial
---


# Chapter 5: Smoke Tests and Mock Infrastructure

Welcome to **Chapter 5: Smoke Tests and Mock Infrastructure**. In this part of **MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains the lightweight test harness used to verify quickstart behavior.

## Learning Goals

- run smoke tests across supported language examples
- use mock client/server helpers for isolated protocol checks
- extend test coverage without external API dependencies
- integrate quickstart tests into CI workflows

## Test Infrastructure Components

| Helper | Role |
|:-------|:-----|
| `mcp-test-client.ts` | probes server readiness and tool listing |
| `mock-mcp-server.ts` | validates client-side protocol calls |
| `smoke-test.sh` | orchestrates cross-runtime checks |

## Source References

- [Smoke Tests Guide](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/tests/README.md)
- [CI Workflow](https://github.com/modelcontextprotocol/quickstart-resources/blob/main/.github/workflows/ci.yml)

## Summary

You now have a repeatable validation loop for quickstart server/client quality.

Next: [Chapter 6: Cross-Language Consistency and Extension Strategy](06-cross-language-consistency-and-extension-strategy.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `mcp-client-typescript/index.ts`

The `main` function in [`mcp-client-typescript/index.ts`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/mcp-client-typescript/index.ts) handles a key part of this chapter's functionality:

```ts
}

async function main() {
  if (process.argv.length < 3) {
    console.log("Usage: node build/index.js <path_to_server_script>");
    return;
  }
  const mcpClient = new MCPClient();
  try {
    await mcpClient.connectToServer(process.argv[2]);

    // Check if we have a valid API key to continue
    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      console.log(
        "\nNo ANTHROPIC_API_KEY found. To query these tools with Claude, set your API key:"
      );
      console.log("  export ANTHROPIC_API_KEY=your-api-key-here");
      return;
    }

    await mcpClient.chatLoop();
  } catch (e) {
    console.error("Error:", e);
    await mcpClient.cleanup();
    process.exit(1);
  } finally {
    await mcpClient.cleanup();
    process.exit(0);
  }
}

```

This function is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.

### `mcp-client-rust/src/main.rs`

The `MCPClient` interface in [`mcp-client-rust/src/main.rs`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/mcp-client-rust/src/main.rs) handles a key part of this chapter's functionality:

```rs
const MODEL_ANTHROPIC: &str = "claude-sonnet-4-20250514";

struct MCPClient {
    anthropic: Client,
    session: Option<RunningService<RoleClient, ()>>,
    tools: Vec<GenaiTool>,
}

impl MCPClient {
    fn new() -> Result<Self> {
        Ok(MCPClient {
            anthropic: Client::default(),
            session: None,
            tools: Vec::new(),
        })
    }

    async fn connect_to_server(&mut self, server_args: &[String]) -> Result<()> {
        if self.session.is_some() {
            bail!("Client is already connected to a server");
        }

        let mut command = Command::new(&server_args[0]);
        command.args(&server_args[1..]);

        let process = TokioChildProcess::new(command)
            .with_context(|| format!("Failed to spawn server process for {:?}", server_args))?;

        let session = ().serve(process).await?;

        let rmcp_tools = session
            .list_all_tools()
```

This interface is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.

### `weather-server-typescript/src/index.ts`

The `formatAlert` function in [`weather-server-typescript/src/index.ts`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/weather-server-typescript/src/index.ts) handles a key part of this chapter's functionality:

```ts

// Format alert data
function formatAlert(feature: AlertFeature): string {
  const props = feature.properties;
  return [
    `Event: ${props.event || "Unknown"}`,
    `Area: ${props.areaDesc || "Unknown"}`,
    `Severity: ${props.severity || "Unknown"}`,
    `Status: ${props.status || "Unknown"}`,
    `Headline: ${props.headline || "No headline"}`,
    "---",
  ].join("\n");
}

interface ForecastPeriod {
  name?: string;
  temperature?: number;
  temperatureUnit?: string;
  windSpeed?: string;
  windDirection?: string;
  shortForecast?: string;
}

interface AlertsResponse {
  features: AlertFeature[];
}

interface PointsResponse {
  properties: {
    forecast?: string;
  };
}
```

This function is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.

### `weather-server-typescript/src/index.ts`

The `main` function in [`weather-server-typescript/src/index.ts`](https://github.com/modelcontextprotocol/quickstart-resources/blob/HEAD/weather-server-typescript/src/index.ts) handles a key part of this chapter's functionality:

```ts

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});

```

This function is important because it defines how MCP Quickstart Resources Tutorial: Cross-Language MCP Servers and Clients by Example implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[main]
    B[MCPClient]
    C[formatAlert]
    D[main]
    E[AlertFeature]
    A --> B
    B --> C
    C --> D
    D --> E
```
