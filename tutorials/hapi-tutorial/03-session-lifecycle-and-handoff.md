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

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [HAPI Repository](https://github.com/tiann/hapi)
  Why it matters: authoritative reference on `HAPI Repository` (github.com).
- [HAPI Releases](https://github.com/tiann/hapi/releases)
  Why it matters: authoritative reference on `HAPI Releases` (github.com).
- [HAPI Docs](https://hapi.run)
  Why it matters: authoritative reference on `HAPI Docs` (hapi.run).

Suggested trace strategy:
- search upstream code for `graph` and `Start` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](README.md)
- [Previous Chapter: Chapter 2: System Architecture](02-system-architecture.md)
- [Next Chapter: Chapter 4: Remote Access and Networking](04-remote-access-and-networking.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `hub/scripts/cleanup-sessions.ts`

The `deleteSessions` function in [`hub/scripts/cleanup-sessions.ts`](https://github.com/tiann/hapi/blob/HEAD/hub/scripts/cleanup-sessions.ts) handles a key part of this chapter's functionality:

```ts

// Delete sessions by IDs
function deleteSessions(db: Database, ids: string[]): number {
    if (ids.length === 0) return 0

    const placeholders = ids.map(() => '?').join(', ')
    db.run(`DELETE FROM sessions WHERE id IN (${placeholders})`, ids)
    return ids.length
}

// Main function
async function main(): Promise<void> {
    const { minMessages, pathPattern, messagePattern, orphaned, force, help } = parseArgs()

    if (help) {
        console.log(`
Usage: bun run hub/scripts/cleanup-sessions.ts [options]

Options:
  --min-messages=N   Delete sessions with fewer than N messages (default: 5)
  --path=PATTERN     Delete sessions matching path pattern (glob supported)
  --message=PATTERN  Delete sessions whose first message contains PATTERN (case-insensitive)
  --orphaned         Delete sessions whose path no longer exists
  --force            Skip confirmation prompt
  --help             Show this help message

Filtering logic:
  - Only --min-messages: Delete sessions with message count < N
  - Only --path: Delete ALL sessions matching the path pattern
  - Only --message: Delete sessions whose first user message contains the pattern
  - Only --orphaned: Delete sessions whose path does not exist on filesystem
  - Multiple filters: Delete sessions matching ALL conditions (AND)
```

This function is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.

### `hub/scripts/cleanup-sessions.ts`

The `main` function in [`hub/scripts/cleanup-sessions.ts`](https://github.com/tiann/hapi/blob/HEAD/hub/scripts/cleanup-sessions.ts) handles a key part of this chapter's functionality:

```ts

// Main function
async function main(): Promise<void> {
    const { minMessages, pathPattern, messagePattern, orphaned, force, help } = parseArgs()

    if (help) {
        console.log(`
Usage: bun run hub/scripts/cleanup-sessions.ts [options]

Options:
  --min-messages=N   Delete sessions with fewer than N messages (default: 5)
  --path=PATTERN     Delete sessions matching path pattern (glob supported)
  --message=PATTERN  Delete sessions whose first message contains PATTERN (case-insensitive)
  --orphaned         Delete sessions whose path no longer exists
  --force            Skip confirmation prompt
  --help             Show this help message

Filtering logic:
  - Only --min-messages: Delete sessions with message count < N
  - Only --path: Delete ALL sessions matching the path pattern
  - Only --message: Delete sessions whose first user message contains the pattern
  - Only --orphaned: Delete sessions whose path does not exist on filesystem
  - Multiple filters: Delete sessions matching ALL conditions (AND)

Examples:
  bun run hub/scripts/cleanup-sessions.ts
  bun run hub/scripts/cleanup-sessions.ts --min-messages=3
  bun run hub/scripts/cleanup-sessions.ts --path="/tmp/*"
  bun run hub/scripts/cleanup-sessions.ts --message="hello"
  bun run hub/scripts/cleanup-sessions.ts --orphaned
  bun run hub/scripts/cleanup-sessions.ts --orphaned --min-messages=5 --force
`)
```

This function is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.

### `hub/scripts/cleanup-sessions.ts`

The `SessionInfo` interface in [`hub/scripts/cleanup-sessions.ts`](https://github.com/tiann/hapi/blob/HEAD/hub/scripts/cleanup-sessions.ts) handles a key part of this chapter's functionality:

```ts

// Session info for display
interface SessionInfo {
    id: string
    title: string | null
    firstUserMessage: string | null
    path: string | null
    updatedAt: number
    messageCount: number
}

// Query sessions with message counts
function querySessions(db: Database): SessionInfo[] {
    // Get basic session info
    const sessionRows = db.query<
        { id: string; metadata: string | null; updated_at: number; message_count: number },
        []
    >(`
        SELECT
            s.id,
            s.metadata,
            s.updated_at,
            COUNT(m.id) as message_count
        FROM sessions s
        LEFT JOIN messages m ON m.session_id = s.id
        GROUP BY s.id
    `).all()

    // Get all messages for processing
    const messageRows = db.query<
        { session_id: string; content: string; seq: number },
        []
```

This interface is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.

### `web/src/router.tsx`

The `BackIcon` function in [`web/src/router.tsx`](https://github.com/tiann/hapi/blob/HEAD/web/src/router.tsx) handles a key part of this chapter's functionality:

```tsx
import SettingsPage from '@/routes/settings'

function BackIcon(props: { className?: string }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={props.className}
        >
            <polyline points="15 18 9 12 15 6" />
        </svg>
    )
}

function PlusIcon(props: { className?: string }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
```

This function is important because it defines how HAPI Tutorial: Remote Control for Local AI Coding Sessions implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[deleteSessions]
    B[main]
    C[SessionInfo]
    D[BackIcon]
    E[PlusIcon]
    A --> B
    B --> C
    C --> D
    D --> E
```
