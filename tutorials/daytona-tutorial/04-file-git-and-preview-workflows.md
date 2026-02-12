---
layout: default
title: "Chapter 4: File, Git, and Preview Workflows"
nav_order: 4
parent: Daytona Tutorial
---

# Chapter 4: File, Git, and Preview Workflows

This chapter maps the day-to-day development workflow inside Daytona sandboxes.

## Learning Goals

- manage file uploads, downloads, and directory operations
- clone and manipulate repositories in sandbox contexts
- expose running services with preview links
- keep preview and repo workflows reproducible for agents

## Workflow Pattern

Treat each sandbox as a disposable but scriptable workspace: hydrate files, clone code, run tasks, expose service previews for review, then persist artifacts through snapshots/volumes if needed.

## Source References

- [File System Operations](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/file-system-operations.mdx)
- [Git Operations](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/git-operations.mdx)
- [Preview](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/preview.mdx)
- [Webhooks](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/webhooks.mdx)

## Summary

You can now run a full code-to-preview loop inside Daytona with cleaner automation boundaries.

Next: [Chapter 5: MCP Agent Integration and Tooling](05-mcp-agent-integration-and-tooling.md)
