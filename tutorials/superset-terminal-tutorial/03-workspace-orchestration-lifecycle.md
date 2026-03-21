---
layout: default
title: "Chapter 3: Workspace Orchestration Lifecycle"
nav_order: 3
parent: Superset Terminal Tutorial
---


# Chapter 3: Workspace Orchestration Lifecycle

Welcome to **Chapter 3: Workspace Orchestration Lifecycle**. In this part of **Superset Terminal Tutorial: Command Center for Parallel Coding Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Superset orchestrates workspace CRUD and related cascade operations for processes and diffs.

## Lifecycle Responsibilities

| Operation | Behavior |
|:----------|:---------|
| create | initialize workspace metadata and select active workspace |
| list/get/update | read and mutate workspace state |
| delete | cascade cleanup of process and diff artifacts |

## Source References

- [Workspace orchestrator implementation](https://github.com/superset-sh/superset/blob/main/apps/cli/src/lib/orchestrators/workspace-orchestrator.ts)
- [Workspace init manager](https://github.com/superset-sh/superset/blob/main/apps/desktop/src/main/lib/workspace-init-manager.ts)

## Summary

You now have a concrete lifecycle model for Superset workspace management.

Next: [Chapter 4: Multi-Agent Program Compatibility](04-multi-agent-program-compatibility.md)

## Source Code Walkthrough

### `bunfig.toml`

The `bunfig` module in [`bunfig.toml`](https://github.com/superset-sh/superset/blob/HEAD/bunfig.toml) handles a key part of this chapter's functionality:

```toml
[install]
linker = "isolated" # Prevent hoisting from resolving `path-scurry@2` to `lru-cache@6` (missing `LRUCache`), which breaks the `@superset/desktop` postinstall native rebuild.

```

This module is important because it defines how Superset Terminal Tutorial: Command Center for Parallel Coding Agents implements the patterns covered in this chapter.

### `.codex/config.toml`

The `config` module in [`.codex/config.toml`](https://github.com/superset-sh/superset/blob/HEAD/.codex/config.toml) handles a key part of this chapter's functionality:

```toml
[mcp_servers.superset]
type = "sse"
url = "https://api.superset.sh/api/agent/mcp"

[mcp_servers.expo-mcp]
type = "sse"
url = "https://mcp.expo.dev/mcp"
enabled = false

[mcp_servers.maestro]
command = "maestro"
args = ["mcp"]

[mcp_servers.neon]
type = "sse"
url = "https://mcp.neon.tech/mcp"

[mcp_servers.linear]
type = "sse"
url = "https://mcp.linear.app/mcp"

[mcp_servers.sentry]
type = "sse"
url = "https://mcp.sentry.dev/mcp"


[mcp_servers.desktop-automation]
command = "bun"
args = ["run", "packages/desktop-mcp/src/bin.ts"]

```

This module is important because it defines how Superset Terminal Tutorial: Command Center for Parallel Coding Agents implements the patterns covered in this chapter.

### `.mcp.json`

The `.mcp` module in [`.mcp.json`](https://github.com/superset-sh/superset/blob/HEAD/.mcp.json) handles a key part of this chapter's functionality:

```json
{
	"mcpServers": {
		"superset": {
			"type": "http",
			"url": "https://api.superset.sh/api/agent/mcp"
		},
		"expo-mcp": {
			"type": "http",
			"url": "https://mcp.expo.dev/mcp",
			"enabled": false
		},
		"maestro": {
			"command": "maestro",
			"args": ["mcp"]
		},
		"neon": {
			"type": "http",
			"url": "https://mcp.neon.tech/mcp"
		},
		"linear": {
			"type": "http",
			"url": "https://mcp.linear.app/mcp"
		},
		"sentry": {
			"type": "http",
			"url": "https://mcp.sentry.dev/mcp"
		},
		"posthog": {
			"type": "http",
			"url": "https://mcp.posthog.com/mcp"
		},
		"desktop-automation": {
			"command": "bun",
			"args": ["run", "packages/desktop-mcp/src/bin.ts"]
		}
```

This module is important because it defines how Superset Terminal Tutorial: Command Center for Parallel Coding Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[bunfig]
    B[config]
    C[.mcp]
    A --> B
    B --> C
```
