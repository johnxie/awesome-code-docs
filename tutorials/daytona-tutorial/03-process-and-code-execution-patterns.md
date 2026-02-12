---
layout: default
title: "Chapter 3: Process and Code Execution Patterns"
nav_order: 3
parent: Daytona Tutorial
---

# Chapter 3: Process and Code Execution Patterns

This chapter covers process execution and code-run workflows across SDK surfaces.

## Learning Goals

- choose stateless versus stateful execution paths
- structure command execution with timeouts and environment variables
- capture stdout/stderr and exit codes for reliable automation
- design retries and error handling for long-running tasks

## Execution Heuristic

Use stateless execution for isolated snippets and predictable idempotent jobs. Use stateful interpreter contexts only when you need persistent variables and iterative sessions. Keep explicit timeout and error handling in both paths.

## Source References

- [Process and Code Execution](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/process-code-execution.mdx)
- [Language Server Protocol](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/language-server-protocol.mdx)
- [Python SDK README](https://github.com/daytonaio/daytona/blob/main/libs/sdk-python/README.md)
- [TypeScript SDK README](https://github.com/daytonaio/daytona/blob/main/libs/sdk-typescript/README.md)

## Summary

You now have an execution model that balances speed, isolation, and observability.

Next: [Chapter 4: File, Git, and Preview Workflows](04-file-git-and-preview-workflows.md)
