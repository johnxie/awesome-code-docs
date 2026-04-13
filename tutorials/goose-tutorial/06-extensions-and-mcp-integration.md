---
layout: default
title: "Chapter 6: Extensions and MCP Integration"
nav_order: 6
parent: Goose Tutorial
---


# Chapter 6: Extensions and MCP Integration

Welcome to **Chapter 6: Extensions and MCP Integration**. In this part of **Goose Tutorial: Extensible Open-Source AI Agent for Real Engineering Work**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers how Goose expands beyond built-ins through MCP extension workflows.

## Learning Goals

- understand Goose extension architecture
- enable and manage built-in extensions safely
- add custom MCP servers via UI or CLI
- standardize extension rollout for teams

## Extension Architecture

```mermaid
flowchart TD
    A["Goose Agent"] --> B["Extension Manager"]
    B --> C["Builtin: Developer\n(crates/goose-mcp/src/)"]
    B --> D["Builtin: Memory\n(crates/goose-mcp/src/memory/)"]
    B --> E["Builtin: Computer Controller\n(crates/goose-mcp/src/computercontroller/)"]
    B --> F["Custom Stdio MCP\n(any MCP-compliant subprocess)"]
    B --> G["Remote StreamableHttp MCP\n(cloud-hosted MCP server)"]
    C --> H["Tools exposed to LLM via ToolRouter"]
    D --> H
    E --> H
    F --> H
    G --> H
```

## Built-In Extension Surface

Goose includes development and platform extensions shipped as part of `crates/goose-mcp/`:

| Extension | Crate Path | Primary Tools |
|:----------|:-----------|:--------------|
| Developer | `src/developer/` | `read_file`, `write_file`, `shell_exec`, `list_directory` |
| Computer Controller | `src/computercontroller/` | screen capture, mouse/keyboard control, browser, PDF/DOCX/XLSX processing |
| Memory | `src/memory/` | `remember_memory`, `retrieve_memories`, `remove_memory_category` |
| AutoVisualiser | `src/autovisualiser/` | auto-generates visualizations from data |
| Tutorial | `src/tutorial/` | in-agent tutorial guidance |

These can be toggled based on task needs to reduce tool overload. Loading fewer extensions means the model sees a smaller tool list, which improves tool selection accuracy for specialized tasks.

## Custom MCP Flow (CLI)

```bash
goose configure
# select: Add Extension
# choose: Command-line Extension OR Remote Extension
```

Example commands for popular community MCP servers:

```bash
# Filesystem access (scoped to a directory)
npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/dir

# GitHub integration
npx -y @modelcontextprotocol/server-github

# Postgres database
npx -y @modelcontextprotocol/server-postgres postgresql://user:pass@host/db

# Brave web search
npx -y @modelcontextprotocol/server-brave-search
```

Each of these spawns as a subprocess that communicates with Goose over stdin/stdout using the MCP protocol. The tools they expose become available to the LLM in the next session.

## Managing Extensions Across Sessions

Extensions added via `goose configure` persist to `~/.config/goose/config.yaml` and load for all future sessions. To use an extension only for a specific session:

```bash
# Only for this session — not persisted
goose session --with-extension "npx -y @modelcontextprotocol/server-github"

# Only for this run — not persisted
goose run --text "..." --with-extension "npx -y @modelcontextprotocol/server-github"
```

To remove a persisted extension, run `goose configure` and select "Remove Extension".

## Extension Types in Detail

Goose supports four distinct extension configuration types:

| Type | When to Use | Example |
|:-----|:------------|:--------|
| `Builtin` | Bundled extensions shipped with Goose | `--with-builtin developer` |
| `Stdio` | Any MCP server communicating over stdin/stdout | `npx @modelcontextprotocol/server-filesystem` |
| `StreamableHttp` | Remote MCP server over HTTP streaming | A deployed cloud MCP endpoint |
| `Platform` | OS-native system extensions | Built into the desktop app |

The `Stdio` type covers the vast majority of community MCP servers. You provide the command and arguments; Goose spawns the process and communicates over the MCP protocol.

## Enabling Extensions at Runtime (CLI)

Extensions can be injected per-invocation without modifying config:

```bash
# Add the developer built-in for this session only
goose session --with-builtin developer

# Add a custom stdio MCP server for this run only
goose run --text "Analyze dependencies" \
  --with-extension "npx -y @modelcontextprotocol/server-filesystem /home/user/project"

# Load a remote streamable HTTP extension
goose session --with-streamable-http-extension "https://my-mcp-server.example.com"
```

Extensions added via flags are not persisted to config. This makes them suitable for CI pipelines where you want a clean, reproducible extension surface.

## The Memory Extension in Depth

The built-in `Memory` extension (in `crates/goose-mcp/src/memory/`) provides persistent tool-backed memory across sessions:

- **`remember_memory`** — stores a key-value pair in a category, optionally tagged
- **`retrieve_memories`** — fetches all memories in a category (use `"*"` for all)
- **`remove_memory_category`** — bulk-deletes a category
- **`remove_specific_memory`** — removes a single entry by content match

Global memories persist in `~/.config/goose/memory/` and survive across projects. Local memories live in `.goose/memory/` within the project directory. This dual-scope model is useful for storing both personal preferences (global) and project-specific conventions (local).

## Extension Safety Checklist

1. review extension command/source before adding
2. set reasonable timeout values (default: 30s)
3. apply `SmartApprove` or `Approve` mode when using new extensions
4. test in a sandbox repository first
5. add extension commands to your team's allowlist policy before broad rollout

## Source References

- [Using Extensions](https://block.github.io/goose/docs/getting-started/using-extensions)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Server Directory](https://www.pulsemcp.com/servers)

## Summary

You now know how to evolve Goose capabilities with built-in and external MCP integrations.

Next: [Chapter 7: CLI Workflows and Automation](07-cli-workflows-and-automation.md)

## How These Components Connect

```mermaid
flowchart TD
    A[Goose agent] --> B{Extension type}
    B -->|Built-in| C[goose --with-builtin developer]
    B -->|Custom MCP| D[goose --with-extension cmd]
    C --> E[Pre-packaged tools: files, shell, browser]
    D --> F[MCP server subprocess spawned]
    F --> G[stdio transport]
    G --> H[Custom tools exposed to agent]
    E --> I[Agent tool calls]
    H --> I
```

## Source Code Walkthrough

### `crates/goose-mcp/src/memory/mod.rs` — built-in Memory extension

The `MemoryServer` struct in [`crates/goose-mcp/src/memory/mod.rs`](https://github.com/block/goose/blob/main/crates/goose-mcp/src/memory/mod.rs) is one of Goose's built-in MCP extensions:

```rust
pub struct MemoryServer {
    tool_router: ToolRouter<Self>,
    instructions: String,
    global_memory_dir: PathBuf,   // ~/.config/goose/memory/
}
```

The four tool parameter types expose the full memory API to the model:

- **`RememberMemoryParams`** — category, data string, optional tags, global/local flag
- **`RetrieveMemoriesParams`** — category (supports `"*"` for all), storage scope
- **`RemoveMemoryCategoryParams`** — wildcard category deletion
- **`RemoveSpecificMemoryParams`** — removes individual items by content match

Context for local vs. global storage is injected via the `extract_working_dir_from_meta()` helper, which reads the `"agent-working-dir"` header from MCP request metadata.

### `crates/goose-server/src/routes/agent.rs` — extension add/remove API

When adding a custom MCP server via the desktop UI, the server calls the `AddExtensionRequest` handler in [`crates/goose-server/src/routes/agent.rs`](https://github.com/block/goose/blob/main/crates/goose-server/src/routes/agent.rs). The payload mirrors the four `ExtensionConfig` variants:

```rust
// POST /extensions/add — for a stdio MCP server:
// {
//   "type": "stdio",
//   "name": "my-extension",
//   "cmd": "npx",
//   "args": ["-y", "@modelcontextprotocol/server-memory"],
//   "timeout": 30
// }
```

The same endpoint handles `Builtin`, `StreamableHttp`, and `Platform` variants by switching on the `type` field.
