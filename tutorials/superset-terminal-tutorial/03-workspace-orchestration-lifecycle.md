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

## Depth Expansion Playbook

## Source Code Walkthrough

### `package.json`

The `package` module in [`package.json`](https://github.com/superset-sh/superset/blob/HEAD/package.json) handles a key part of this chapter's functionality:

```json
{
	"name": "@superset/repo",
	"version": "0.0.0",
	"repository": {
		"type": "git"
	},
	"devDependencies": {
		"@biomejs/biome": "2.4.2",
		"dotenv-cli": "^11.0.0",
		"sherif": "^1.10.0",
		"turbo": "^2.8.7"
	},
	"description": "Superset Monorepo",
	"homepage": "https://superset.sh",
	"license": "Elastic-2.0",
	"packageManager": "bun@1.3.6",
	"private": true,
	"scripts": {
		"dev": "turbo run dev dev:caddy --filter=@superset/api --filter=@superset/web --filter=@superset/desktop --filter=electric-proxy --filter=//",
		"dev:all": "turbo dev",
		"dev:caddy": "dotenv -- caddy run --config Caddyfile",
		"dev:docs": "turbo dev --filter=@superset/docs",
		"dev:marketing": "turbo dev --filter=@superset/marketing --filter=@superset/docs",
		"build": "turbo build --filter=@superset/desktop",
		"test": "turbo test",
		"lint": "./scripts/lint.sh",
		"check:desktop-git-env": "./scripts/check-desktop-git-env.sh",
		"lint:fix": "bunx @biomejs/biome@2.4.2 migrate --write && bunx @biomejs/biome@2.4.2 check --write --unsafe .",
		"format": "bunx @biomejs/biome@2.4.2 format --write .",
		"format:check": "bunx @biomejs/biome@2.4.2 format .",
		"typecheck": "turbo typecheck",
		"ui-add": "turbo run ui-add",
		"postinstall": "./scripts/postinstall.sh",
		"clean": "git clean -xdf node_modules",
		"clean:workspaces": "turbo clean",
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

### `.mastracode/mcp.json`

The `mcp` module in [`.mastracode/mcp.json`](https://github.com/superset-sh/superset/blob/HEAD/.mastracode/mcp.json) handles a key part of this chapter's functionality:

```json
{
	"mcpServers": {
		"superset": {
			"command": "npx",
			"args": ["-y", "mcp-remote", "https://api.superset.sh/api/agent/mcp"]
		},
		"maestro": {
			"command": "maestro",
			"args": ["mcp"]
		},
		"neon": {
			"command": "npx",
			"args": ["-y", "mcp-remote", "https://mcp.neon.tech/mcp"]
		},
		"linear": {
			"command": "npx",
			"args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]
		},
		"sentry": {
			"command": "npx",
			"args": ["-y", "mcp-remote", "https://mcp.sentry.dev/mcp"]
		},
		"desktop-automation": {
			"command": "bun",
			"args": ["run", "packages/desktop-mcp/src/bin.ts"]
		}
	}
}

```

This module is important because it defines how Superset Terminal Tutorial: Command Center for Parallel Coding Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[package]
    B[.mcp]
    C[mcp]
    A --> B
    B --> C
```
