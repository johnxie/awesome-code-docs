---
layout: default
title: "Chapter 4: Sandbox and Preview Runtime"
nav_order: 4
parent: VibeSDK Tutorial
---

# Chapter 4: Sandbox and Preview Runtime

VibeSDK runs generated projects in isolated preview runtimes so users can validate behavior before publishing.

## Learning Goals

By the end of this chapter, you should be able to:

- explain how generated code becomes a live preview URL
- tune sandbox capacity and runtime controls
- separate sandbox/runtime failures from generation-quality issues
- design a basic incident response flow for preview instability

## Runtime Flow

1. agent finishes a generation stage with runnable outputs
2. sandbox orchestration spins up or assigns a runtime instance
3. preview routing returns a URL to user session
4. runtime logs and errors feed back into fix loops
5. stable results can be promoted to deployment actions

## Isolation Model

```mermaid
graph TD
    A[Generation Agent] --> B[Sandbox Orchestrator]
    B --> C[Container Runtime]
    C --> D[Preview URL]
    D --> E[User Feedback]
    E --> A
```

## Core Runtime Controls

| Control | Why It Exists | Tuning Guidance |
|:--------|:--------------|:----------------|
| `SANDBOX_INSTANCE_TYPE` | defines CPU/RAM profile | start conservative, raise only when startup/latency data justifies |
| `MAX_SANDBOX_INSTANCES` | caps concurrent preview capacity | align with expected user concurrency and budget limits |
| tunnel/preview settings | controls preview reachability | keep defaults initially, change only with verified need |
| dispatch/deployment bindings | enables app handoff from preview to deploy | validate early in staging to avoid late surprises |

## Operational Baseline Metrics

Track these together, not in isolation:

- preview startup latency (p50 and p95)
- runtime restart/crash rate
- concurrent active preview count
- preview availability success rate
- cost per preview hour

## Triage: Generation vs Runtime

| Symptom | Likely Layer | First Check |
|:--------|:-------------|:------------|
| files look wrong before preview | generation pipeline | phase outputs and model routing |
| preview never starts | runtime/orchestration | sandbox logs and instance quotas |
| preview starts then dies | runtime stability | container restarts and resource pressure |
| preview works, deploy fails | deployment bindings/policy | dispatch namespace and credentials |

## Hardening Practices

- enforce idle cleanup and timeout policies
- isolate noisy tenant workloads when concurrency spikes
- keep a safe fallback instance profile
- include preview health in user-visible status telemetry

## Source References

- [VibeSDK Setup Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/setup.md)
- [Architecture Diagrams](https://github.com/cloudflare/vibesdk/blob/main/docs/architecture-diagrams.md)

## Summary

You now have a runtime model for sandbox previews and a practical baseline for stability tuning.

Next: [Chapter 5: Data Layer and Persistence](05-data-layer-and-persistence.md)
