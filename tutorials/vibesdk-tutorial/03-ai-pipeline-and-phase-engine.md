---
layout: default
title: "Chapter 3: AI Pipeline and Phase Engine"
nav_order: 3
parent: VibeSDK Tutorial
---


# Chapter 3: AI Pipeline and Phase Engine

Welcome to **Chapter 3: AI Pipeline and Phase Engine**. In this part of **VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


VibeSDK uses a structured phase engine so generation is auditable, recoverable, and tunable instead of a one-shot black box.

## Learning Goals

By the end of this chapter, you should be able to:

- explain each generation stage and its output
- tune model/provider choices by operation type
- apply phase-gate criteria to improve delivery quality
- understand fallback and recovery behavior under provider instability

## Pipeline Overview

```mermaid
graph LR
    P[User Prompt] --> B[Blueprint]
    B --> G[Phase Planning]
    G --> I[Implementation]
    I --> R[Review and Validation]
    R --> F[Fix Loop]
    F --> D[Deployable Result]
```

## Operation Types and Intent

| Operation | Purpose | Typical Failure Mode |
|:----------|:--------|:---------------------|
| blueprint generation | convert product intent into architecture and scope | over-broad or under-constrained plans |
| phase planning | sequence milestones and dependencies | phase granularity too coarse |
| implementation | generate concrete file-level outputs | partial/inconsistent file sets |
| review and validation | detect runtime or structural issues | shallow checks miss integration failures |
| fix loops | repair targeted failures quickly | oscillating fixes when root cause is unclear |

## Model Routing and Provider Strategy

Model/provider behavior is configured at operation level in `worker/agents/inferutils/config.ts`.

Recommended approach:

- keep a known-good default provider/model pair per operation
- define explicit fallback routes for provider/API outages
- test changes per operation, not globally
- track quality and cost by operation type

## Phase Gate Criteria (Practical)

Move to next phase only when all are true:

1. expected phase artifacts are produced
2. validation signals are green for touched scope
3. unresolved risks are documented with severity and owner
4. rollback path is known if downstream phase fails

## Quality Controls That Matter Most

- bounded prompts per phase reduce drift
- explicit artifacts improve auditability
- deterministic phase transitions reduce unreproducible failures
- short fix loops improve mean time to usable preview

## Debugging Playbook

If generation quality regresses:

1. isolate which operation regressed (blueprint/phase/impl/review/fix)
2. compare provider/model route for that operation
3. inspect prompt inputs and context payload size
4. replay with constrained scope before full prompt retry
5. update fallback policy when instability is provider-specific

## Source References

- [VibeSDK LLM Developer Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/llm.md)
- [VibeSDK Repository](https://github.com/cloudflare/vibesdk)

## Summary

You now understand how VibeSDK decomposes app generation into controllable phases and where to tune for reliability.

Next: [Chapter 4: Sandbox and Preview Runtime](04-sandbox-and-preview-runtime.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `container/cli-tools.ts`

The `main` function in [`container/cli-tools.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/container/cli-tools.ts) handles a key part of this chapter's functionality:

```ts
}

async function main() {
  try {
    // Initialize data directory
    initializeDataDirectory();
    
    const { values: args, positionals } = parseArgs({
      args: process.argv.slice(2),
      options: {
        // Global options
        'instance-id': { type: 'string', short: 'i' },
        'format': { type: 'string' },
        'db-path': { type: 'string' },
        'help': { type: 'boolean', short: 'h' },
        
        // Process options
        'cwd': { type: 'string', short: 'c' },
        'port': { type: 'string', short: 'p' },
        'max-restarts': { type: 'string' },
        'restart-delay': { type: 'string' },
        'health-check-interval': { type: 'string' },
        'max-errors': { type: 'string' },
        'retention-days': { type: 'string' },
        'log-retention-hours': { type: 'string' },
        'force': { type: 'boolean' },
        
        // Filter options
        'levels': { type: 'string' },
        'streams': { type: 'string' },
        'categories': { type: 'string' },
        'severities': { type: 'string' },
```

This function is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `container/cli-tools.ts`

The `handleProcessCommand` function in [`container/cli-tools.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/container/cli-tools.ts) handles a key part of this chapter's functionality:

```ts
    switch (command) {
      case 'process':
        await handleProcessCommand(subcommand, args, positionals.slice(2));
        break;
        
      case 'errors':
        await handleErrorCommand(subcommand, args);
        break;
        
      case 'logs':
        await handleLogCommand(subcommand, args);
        break;
        
      default:
        OutputFormatter.formatError(`Unknown command: ${command}`);
        showHelp();
        process.exit(1);
    }

  } catch (error) {
    OutputFormatter.formatError(`CLI failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    process.exit(1);
  }
}

async function handleProcessCommand(subcommand: string, args: Record<string, unknown>, remainingArgs: string[]) {
  switch (subcommand) {
    case 'start':
      if (remainingArgs.length === 0) {
        OutputFormatter.formatError('No command specified to monitor');
        process.exit(1);
      }
```

This function is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `container/cli-tools.ts`

The `handleErrorCommand` function in [`container/cli-tools.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/container/cli-tools.ts) handles a key part of this chapter's functionality:

```ts
        
      case 'errors':
        await handleErrorCommand(subcommand, args);
        break;
        
      case 'logs':
        await handleLogCommand(subcommand, args);
        break;
        
      default:
        OutputFormatter.formatError(`Unknown command: ${command}`);
        showHelp();
        process.exit(1);
    }

  } catch (error) {
    OutputFormatter.formatError(`CLI failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    process.exit(1);
  }
}

async function handleProcessCommand(subcommand: string, args: Record<string, unknown>, remainingArgs: string[]) {
  switch (subcommand) {
    case 'start':
      if (remainingArgs.length === 0) {
        OutputFormatter.formatError('No command specified to monitor');
        process.exit(1);
      }

      const instanceId = String(args['instance-id'] || process.env.INSTANCE_ID || `instance-${Date.now()}`);
      validateInstanceId(instanceId);

```

This function is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `container/cli-tools.ts`

The `handleLogCommand` function in [`container/cli-tools.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/container/cli-tools.ts) handles a key part of this chapter's functionality:

```ts
        
      case 'logs':
        await handleLogCommand(subcommand, args);
        break;
        
      default:
        OutputFormatter.formatError(`Unknown command: ${command}`);
        showHelp();
        process.exit(1);
    }

  } catch (error) {
    OutputFormatter.formatError(`CLI failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    process.exit(1);
  }
}

async function handleProcessCommand(subcommand: string, args: Record<string, unknown>, remainingArgs: string[]) {
  switch (subcommand) {
    case 'start':
      if (remainingArgs.length === 0) {
        OutputFormatter.formatError('No command specified to monitor');
        process.exit(1);
      }

      const instanceId = String(args['instance-id'] || process.env.INSTANCE_ID || `instance-${Date.now()}`);
      validateInstanceId(instanceId);

      await ProcessCommands.start({
        instanceId,
        command: remainingArgs[0],
        args: remainingArgs.slice(1),
```

This function is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[main]
    B[handleProcessCommand]
    C[handleErrorCommand]
    D[handleLogCommand]
    E[ContentType]
    A --> B
    B --> C
    C --> D
    D --> E
```
