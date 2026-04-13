---
layout: default
title: "Chapter 4: Configuration, Modes, and Context Injection"
nav_order: 4
parent: Claude-Mem Tutorial
---


# Chapter 4: Configuration, Modes, and Context Injection

Welcome to **Chapter 4: Configuration, Modes, and Context Injection**. In this part of **Claude-Mem Tutorial: Persistent Memory Compression for Claude Code**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers the highest-leverage controls for memory quality and context relevance.

## Learning Goals

- tune core settings in `~/.claude-mem/settings.json`
- configure model/provider options and runtime defaults
- control context injection filters and display behavior
- avoid over-injection and noisy memory surfaces

## Key Configuration Areas

- model/provider selection
- worker and data directory settings
- context injection filtering and presentation
- mode and behavior toggles for memory retrieval

## Configuration Hygiene

- track settings changes in small increments
- validate one config change per session when debugging
- keep project-level context expectations documented

## Source References

- [Configuration Guide](https://docs.claude-mem.ai/configuration)
- [Folder Context Files](https://docs.claude-mem.ai/usage/folder-context)
- [README Configuration](https://github.com/thedotmack/claude-mem/blob/main/README.md#configuration)

## Summary

You now know how to tune Claude-Mem behavior for accurate, low-noise context injection.

Next: [Chapter 5: Search Tools and Progressive Disclosure](05-search-tools-and-progressive-disclosure.md)

## Source Code Walkthrough

### `scripts/fix-corrupted-timestamps.ts`

The `main` function in [`scripts/fix-corrupted-timestamps.ts`](https://github.com/thedotmack/claude-mem/blob/HEAD/scripts/fix-corrupted-timestamps.ts) handles a key part of this chapter's functionality:

```ts
}

function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const autoYes = args.includes('--yes') || args.includes('-y');

  console.log('🔍 Analyzing corrupted observation timestamps...\n');
  if (dryRun) {
    console.log('🏃 DRY RUN MODE - No changes will be made\n');
  }

  const db = new Database(DB_PATH);

  try {
    // Step 1: Find affected observations
    console.log('Step 1: Finding observations created during bad window...');
    const affectedObs = db.query<AffectedObservation, []>(`
      SELECT id, memory_session_id, created_at_epoch, title
      FROM observations
      WHERE created_at_epoch >= ${BAD_WINDOW_START}
        AND created_at_epoch <= ${BAD_WINDOW_END}
      ORDER BY id
    `).all();

    console.log(`Found ${affectedObs.length} observations in bad window\n`);

    if (affectedObs.length === 0) {
      console.log('✅ No affected observations found!');
      return;
    }

```

This function is important because it defines how Claude-Mem Tutorial: Persistent Memory Compression for Claude Code implements the patterns covered in this chapter.

### `scripts/fix-corrupted-timestamps.ts`

The `applyFixes` function in [`scripts/fix-corrupted-timestamps.ts`](https://github.com/thedotmack/claude-mem/blob/HEAD/scripts/fix-corrupted-timestamps.ts) handles a key part of this chapter's functionality:

```ts
    if (autoYes) {
      console.log('Auto-confirming with --yes flag...\n');
      applyFixes(db, fixes);
      return;
    }

    console.log('Apply these fixes? (y/n): ');

    const stdin = Bun.stdin.stream();
    const reader = stdin.getReader();

    reader.read().then(({ value }) => {
      const response = new TextDecoder().decode(value).trim().toLowerCase();

      if (response === 'y' || response === 'yes') {
        applyFixes(db, fixes);
      } else {
        console.log('\n❌ Fixes cancelled. No changes made.');
        db.close();
      }
    });

  } catch (error) {
    console.error('❌ Error:', error);
    db.close();
    process.exit(1);
  }
}

function applyFixes(db: Database, fixes: TimestampFix[]) {
  console.log('\n🔧 Applying fixes...\n');

```

This function is important because it defines how Claude-Mem Tutorial: Persistent Memory Compression for Claude Code implements the patterns covered in this chapter.

### `scripts/fix-corrupted-timestamps.ts`

The `AffectedObservation` interface in [`scripts/fix-corrupted-timestamps.ts`](https://github.com/thedotmack/claude-mem/blob/HEAD/scripts/fix-corrupted-timestamps.ts) handles a key part of this chapter's functionality:

```ts
const BAD_WINDOW_END = 1766626260000;   // Dec 24 20:31 PST

interface AffectedObservation {
  id: number;
  memory_session_id: string;
  created_at_epoch: number;
  title: string;
}

interface ProcessedMessage {
  id: number;
  session_db_id: number;
  tool_name: string;
  created_at_epoch: number;
  completed_at_epoch: number;
}

interface SessionMapping {
  session_db_id: number;
  memory_session_id: string;
}

interface TimestampFix {
  observation_id: number;
  observation_title: string;
  wrong_timestamp: number;
  correct_timestamp: number;
  session_db_id: number;
  pending_message_id: number;
}

function formatTimestamp(epoch: number): string {
```

This interface is important because it defines how Claude-Mem Tutorial: Persistent Memory Compression for Claude Code implements the patterns covered in this chapter.

### `scripts/fix-corrupted-timestamps.ts`

The `ProcessedMessage` interface in [`scripts/fix-corrupted-timestamps.ts`](https://github.com/thedotmack/claude-mem/blob/HEAD/scripts/fix-corrupted-timestamps.ts) handles a key part of this chapter's functionality:

```ts
}

interface ProcessedMessage {
  id: number;
  session_db_id: number;
  tool_name: string;
  created_at_epoch: number;
  completed_at_epoch: number;
}

interface SessionMapping {
  session_db_id: number;
  memory_session_id: string;
}

interface TimestampFix {
  observation_id: number;
  observation_title: string;
  wrong_timestamp: number;
  correct_timestamp: number;
  session_db_id: number;
  pending_message_id: number;
}

function formatTimestamp(epoch: number): string {
  return new Date(epoch).toLocaleString('en-US', {
    timeZone: 'America/Los_Angeles',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
```

This interface is important because it defines how Claude-Mem Tutorial: Persistent Memory Compression for Claude Code implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[main]
    B[applyFixes]
    C[AffectedObservation]
    D[ProcessedMessage]
    E[SessionMapping]
    A --> B
    B --> C
    C --> D
    D --> E
```
