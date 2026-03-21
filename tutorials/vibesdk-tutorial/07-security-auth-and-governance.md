---
layout: default
title: "Chapter 7: Security, Auth, and Governance"
nav_order: 7
parent: VibeSDK Tutorial
---


# Chapter 7: Security, Auth, and Governance

Welcome to **Chapter 7: Security, Auth, and Governance**. In this part of **VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


VibeSDK security is a cross-layer concern: identity, secret management, execution controls, and policy enforcement all matter.

## Learning Goals

By the end of this chapter, you should be able to:

- define a baseline security posture for multi-user VibeSDK environments
- separate auth, token, and secret responsibilities clearly
- design governance checks for model/provider and deployment changes
- prepare recurring operational audits and incident drills

## Security Domains

| Domain | Core Controls |
|:-------|:--------------|
| identity and access | OAuth/email auth flows, session guardrails, role-aware endpoints |
| token/session integrity | JWT signing controls, token rotation cadence, revocation paths |
| secret management | least-privilege API keys, env isolation, secure secret distribution |
| abuse prevention | rate limits, quota caps, workload isolation |
| change governance | review gates for model routing, deployment bindings, policy updates |

## Deployment-Level Security Controls

At minimum, enforce:

- separate credentials for dev/stage/prod
- explicit Cloudflare API token scopes (avoid overbroad tokens)
- environment-specific rate-limit bindings
- clear default-deny behavior for sensitive operations

## Governance Practices That Scale

1. require review for changes in `worker/agents/inferutils/config.ts`
2. log deployment and generation actions with actor identity
3. document retention/deletion policy for generated artifacts and logs
4. tie emergency rollback procedures to named on-call owners

## Security Runbook Checks

| Check | Frequency | Owner |
|:------|:----------|:------|
| secret/token rotation audit | monthly | platform security |
| permission drift review | bi-weekly | platform engineering |
| auth anomaly triage | daily | on-call engineer |
| rollback simulation | quarterly | incident response team |

## High-Risk Mistakes to Avoid

- sharing production API tokens in developer-local environments
- enabling broad provider access without per-environment controls
- skipping review on model/provider fallback changes
- missing retention policies for sensitive generation artifacts

## Source References

- [VibeSDK Setup Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/setup.md)
- [VibeSDK LLM Developer Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/llm.md)

## Summary

You now have a practical security and governance baseline for operating VibeSDK beyond a single-user demo setup.

Next: [Chapter 8: Production Operations and Scaling](08-production-operations-and-scaling.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `scripts/undeploy.ts`

The `CloudflareUndeploymentManager` class in [`scripts/undeploy.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/scripts/undeploy.ts) handles a key part of this chapter's functionality:

```ts
}

class CloudflareUndeploymentManager {
  private config: WranglerConfig;
  private forceMode: boolean = false;
  private allMode: boolean = false;

  constructor() {
    this.parseArguments();
    this.config = this.parseWranglerConfig();
  }

  /**
   * Parse command line arguments
   */
  private parseArguments(): void {
    const args = process.argv.slice(2);
    this.allMode = args.includes('all');
    this.forceMode = args.includes('--force');

    if (this.allMode && !this.forceMode) {
      console.warn('⚠️  Warning: "all" mode requires --force flag for safety');
      console.warn('   Usage: bun scripts/undeploy.ts all --force');
      process.exit(1);
    }

    console.log(`🚨 Undeployment Mode: ${this.allMode ? 'COMPLETE DESTRUCTION' : 'Standard Cleanup'}`);
    if (this.allMode) {
      console.log('⚠️  This will DELETE ALL RESOURCES including D1 database and dispatch namespace!');
    } else {
      console.log('ℹ️  This will preserve D1 database and dispatch namespace');
    }
```

This class is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `scripts/undeploy.ts`

The `WranglerConfig` interface in [`scripts/undeploy.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/scripts/undeploy.ts) handles a key part of this chapter's functionality:

```ts

// Types for configuration
interface WranglerConfig {
  name: string;
  dispatch_namespaces?: Array<{
    binding: string;
    namespace: string;
    experimental_remote?: boolean;
  }>;
  r2_buckets?: Array<{
    binding: string;
    bucket_name: string;
    experimental_remote?: boolean;
  }>;
  containers?: Array<{
    class_name: string;
    image: string;
    max_instances: number;
  }>;
  d1_databases?: Array<{
    binding: string;
    database_name: string;
    database_id: string;
    migrations_dir?: string;
    experimental_remote?: boolean;
  }>;
  kv_namespaces?: Array<{
    binding: string;
    id: string;
    experimental_remote?: boolean;
  }>;
}
```

This interface is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `container/types.ts`

The `LogLine` interface in [`container/types.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/container/types.ts) handles a key part of this chapter's functionality:

```ts
// ==========================================

export interface LogLine {
  readonly content: string;
  readonly timestamp: Date;
  readonly stream: StreamType;
  readonly processId: string;
}

// ==========================================
// STORAGE SCHEMAS - Extend base types
// ==========================================

// StoredError extends SimpleError with storage-specific fields
export const StoredErrorSchema = SimpleErrorSchema.extend({
  id: z.number(),
  instanceId: z.string(),
  processId: z.string(),
  errorHash: z.string(),
  occurrenceCount: z.number(),
  createdAt: z.string()
});
export type StoredError = z.infer<typeof StoredErrorSchema>;

// Base fields shared by stored entities
const StoredEntityBaseSchema = z.object({
  id: z.number(),
  instanceId: z.string(),
  processId: z.string(),
  timestamp: z.string(),
  createdAt: z.string()
});
```

This interface is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `container/types.ts`

The `ProcessInfo` interface in [`container/types.ts`](https://github.com/cloudflare/vibesdk/blob/HEAD/container/types.ts) handles a key part of this chapter's functionality:

```ts
export type ProcessState = z.infer<typeof ProcessStateSchema>;

export interface ProcessInfo {
  readonly id: string;
  readonly instanceId: string;
  readonly command: string;
  readonly args?: readonly string[];
  readonly cwd: string;
  pid?: number;
  readonly env?: Record<string, string>;
  readonly startTime?: Date;
  readonly status?: ProcessState;
  readonly endTime?: Date;
  readonly exitCode?: number;
  readonly restartCount: number;
  readonly lastError?: string;
}

export interface MonitoringOptions {
  readonly autoRestart?: boolean;
  readonly maxRestarts?: number;
  readonly restartDelay?: number;
  readonly healthCheckInterval?: number;
  readonly errorBufferSize?: number;
  readonly env?: Record<string, string>;
  readonly killTimeout?: number;
  readonly expectedPort?: number; // Port the child process should bind to (for health checks)
}

// ==========================================
// STORAGE OPTIONS
// ==========================================
```

This interface is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[CloudflareUndeploymentManager]
    B[WranglerConfig]
    C[LogLine]
    D[ProcessInfo]
    E[MonitoringOptions]
    A --> B
    B --> C
    C --> D
    D --> E
```
