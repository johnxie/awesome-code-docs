---
layout: default
title: "Chapter 3: Session Lifecycle and Handoff"
nav_order: 3
parent: HAPI Tutorial
---


# Chapter 3: Session Lifecycle and Handoff

Welcome to **Chapter 3: Session Lifecycle and Handoff**. In this part of **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


HAPI's key design goal is switching control surfaces without restarting or losing session context.

## Lifecycle Flow

```mermaid
graph LR
    A[Start hapi in terminal] --> B[Session registered in hub]
    B --> C[Remote client attaches]
    C --> D[Messages and approvals flow]
    D --> E[Control switches local <-> remote]
```

## Handoff Rules

- local and remote operate on the same persisted session state
- permission decisions are relayed in real time
- switching surfaces should not fork or duplicate session identity

## High-Value Use Cases

| Use Case | Benefit |
|:---------|:--------|
| stepping away mid-task | continue approvals from phone |
| long-running agent work | monitor status without terminal lock |
| team/operator handoff | preserve continuity during shift changes |

## Summary

You can now model HAPI sessions as persistent control channels, not transient terminal jobs.

Next: [Chapter 4: Remote Access and Networking](04-remote-access-and-networking.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `graph`, `Start`, `hapi` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Session Lifecycle and Handoff` as an operating subsystem inside **HAPI Tutorial: Remote Control for Local AI Coding Sessions**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `terminal`, `Session`, `registered` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Session Lifecycle and Handoff` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `graph`.
2. **Input normalization**: shape incoming data so `Start` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `hapi`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Chapter Connections

- [Tutorial Index](README.md)
- [Previous Chapter: Chapter 2: System Architecture](02-system-architecture.md)
- [Next Chapter: Chapter 4: Remote Access and Networking](04-remote-access-and-networking.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

## Source Code Walkthrough

### `hub/scripts/cleanup-sessions.ts`

The `formatDate` function in [`hub/scripts/cleanup-sessions.ts`](https://github.com/tiann/hapi/blob/HEAD/hub/scripts/cleanup-sessions.ts) handles a key part of this chapter's functionality:

```ts

// Format timestamp as human-readable date
function formatDate(timestamp: number): string {
    const date = new Date(timestamp)
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    })
}

// Truncate string to max length with ellipsis
function truncate(str: string, maxLen: number): string {
    if (str.length <= maxLen) return str
    return str.slice(0, maxLen - 3) + '...'
}

// Extract text from user message content
function extractUserText(content: unknown): string | null {
    if (!content || typeof content !== 'object') return null
    const c = content as Record<string, unknown>
    if (c.role !== 'user') return null
    const inner = c.content
    // Handle { content: { type: 'text', text: '...' } }
    if (inner && typeof inner === 'object') {
        const textObj = inner as Record<string, unknown>
        if (textObj.type === 'text' && typeof textObj.text === 'string') {
            return textObj.text
        }
    }
    // Handle { content: '...' } (string)
    if (typeof inner === 'string') {
```

This function is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.

### `hub/scripts/cleanup-sessions.ts`

The `truncate` function in [`hub/scripts/cleanup-sessions.ts`](https://github.com/tiann/hapi/blob/HEAD/hub/scripts/cleanup-sessions.ts) handles a key part of this chapter's functionality:

```ts

// Truncate string to max length with ellipsis
function truncate(str: string, maxLen: number): string {
    if (str.length <= maxLen) return str
    return str.slice(0, maxLen - 3) + '...'
}

// Extract text from user message content
function extractUserText(content: unknown): string | null {
    if (!content || typeof content !== 'object') return null
    const c = content as Record<string, unknown>
    if (c.role !== 'user') return null
    const inner = c.content
    // Handle { content: { type: 'text', text: '...' } }
    if (inner && typeof inner === 'object') {
        const textObj = inner as Record<string, unknown>
        if (textObj.type === 'text' && typeof textObj.text === 'string') {
            return textObj.text
        }
    }
    // Handle { content: '...' } (string)
    if (typeof inner === 'string') {
        return inner
    }
    return null
}

// Parse command line arguments
function parseArgs(): { minMessages: number | null; pathPattern: string | null; messagePattern: string | null; orphaned: boolean; force: boolean; help: boolean } {
    const args = process.argv.slice(2)
    let minMessages: number | null = null
    let pathPattern: string | null = null
```

This function is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.

### `hub/scripts/cleanup-sessions.ts`

The `extractUserText` function in [`hub/scripts/cleanup-sessions.ts`](https://github.com/tiann/hapi/blob/HEAD/hub/scripts/cleanup-sessions.ts) handles a key part of this chapter's functionality:

```ts

// Extract text from user message content
function extractUserText(content: unknown): string | null {
    if (!content || typeof content !== 'object') return null
    const c = content as Record<string, unknown>
    if (c.role !== 'user') return null
    const inner = c.content
    // Handle { content: { type: 'text', text: '...' } }
    if (inner && typeof inner === 'object') {
        const textObj = inner as Record<string, unknown>
        if (textObj.type === 'text' && typeof textObj.text === 'string') {
            return textObj.text
        }
    }
    // Handle { content: '...' } (string)
    if (typeof inner === 'string') {
        return inner
    }
    return null
}

// Parse command line arguments
function parseArgs(): { minMessages: number | null; pathPattern: string | null; messagePattern: string | null; orphaned: boolean; force: boolean; help: boolean } {
    const args = process.argv.slice(2)
    let minMessages: number | null = null
    let pathPattern: string | null = null
    let messagePattern: string | null = null
    let orphaned = false
    let force = false
    let help = false

    for (const arg of args) {
```

This function is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.

### `hub/scripts/cleanup-sessions.ts`

The `parseArgs` function in [`hub/scripts/cleanup-sessions.ts`](https://github.com/tiann/hapi/blob/HEAD/hub/scripts/cleanup-sessions.ts) handles a key part of this chapter's functionality:

```ts

// Parse command line arguments
function parseArgs(): { minMessages: number | null; pathPattern: string | null; messagePattern: string | null; orphaned: boolean; force: boolean; help: boolean } {
    const args = process.argv.slice(2)
    let minMessages: number | null = null
    let pathPattern: string | null = null
    let messagePattern: string | null = null
    let orphaned = false
    let force = false
    let help = false

    for (const arg of args) {
        if (arg === '--help' || arg === '-h') {
            help = true
        } else if (arg === '--force' || arg === '-f') {
            force = true
        } else if (arg === '--orphaned') {
            orphaned = true
        } else if (arg.startsWith('--min-messages=')) {
            const value = parseInt(arg.split('=')[1], 10)
            if (isNaN(value) || value < 0) {
                console.error('Error: --min-messages must be a non-negative integer')
                process.exit(1)
            }
            minMessages = value
        } else if (arg.startsWith('--path=')) {
            pathPattern = arg.split('=').slice(1).join('=') // Handle paths with '='
        } else if (arg.startsWith('--message=')) {
            messagePattern = arg.split('=').slice(1).join('=').toLowerCase()
        } else {
            console.error(`Unknown argument: ${arg}`)
            console.error('Use --help for usage information')
```

This function is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[formatDate]
    B[truncate]
    C[extractUserText]
    D[parseArgs]
    E[getDbPath]
    A --> B
    B --> C
    C --> D
    D --> E
```
