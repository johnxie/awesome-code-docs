---
layout: default
title: "Chapter 8: Production Team Operations"
nav_order: 8
parent: Superset Terminal Tutorial
---


# Chapter 8: Production Team Operations

Welcome to **Chapter 8: Production Team Operations**. In this part of **Superset Terminal Tutorial: Command Center for Parallel Coding Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Team adoption of Superset needs explicit standards for workspace ownership, quality gates, and agent policy.

## Team Checklist

1. define workspace naming and ownership conventions
2. enforce review before branch merge from agent output
3. standardize setup/teardown scripts for reproducibility
4. set limits for number of concurrent agents per machine
5. track release changes and roll out incrementally

## Source References

- [Superset README](https://github.com/superset-sh/superset/blob/main/README.md)
- [Superset releases](https://github.com/superset-sh/superset/releases)

## Summary

You now have an operations baseline for running Superset as a team-scale multi-agent command center.

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
