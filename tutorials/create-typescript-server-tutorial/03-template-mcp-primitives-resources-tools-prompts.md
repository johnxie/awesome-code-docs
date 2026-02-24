---
layout: default
title: "Chapter 3: Template MCP Primitives: Resources, Tools, Prompts"
nav_order: 3
parent: Create TypeScript Server Tutorial
---

# Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

Welcome to **Chapter 3: Template MCP Primitives: Resources, Tools, Prompts**. In this part of **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter examines generated primitive handlers and protocol mapping.

## Learning Goals

- inspect generated resource/tool/prompt examples
- understand handler signatures and data contracts
- extend primitive logic while preserving MCP semantics
- avoid schema drift during customization

## Source References

- [Template Server Source](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/src/index.ts.ejs)
- [Template README](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/README.md.ejs)

## Summary

You now have a primitive-level model for evolving generated TypeScript server code.

Next: [Chapter 4: Configuration, Metadata, and Packaging](04-configuration-metadata-and-packaging.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- tutorial slug: **create-typescript-server-tutorial**
- chapter focus: **Chapter 3: Template MCP Primitives: Resources, Tools, Prompts**
- system context: **Create Typescript Server Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 3: Template MCP Primitives: Resources, Tools, Prompts`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [Create TypeScript Server README](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/README.md)
- [Template README](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/README.md.ejs)
- [Template Server Source](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/src/index.ts.ejs)
- [Template Package Metadata](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/package.json.ejs)
- [Contributing Guide](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/CONTRIBUTING.md)
- [Security Policy](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/SECURITY.md)

### Cross-Tutorial Connection Map

- [MCP TypeScript SDK Tutorial](../mcp-typescript-sdk-tutorial/)
- [Create Python Server Tutorial](../create-python-server-tutorial/)
- [MCP Quickstart Resources Tutorial](../mcp-quickstart-resources-tutorial/)
- [MCP Servers Tutorial](../mcp-servers-tutorial/)
- [Chapter 1: Getting Started and Scaffolding Flow](01-getting-started-and-scaffolding-flow.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 3: Template MCP Primitives: Resources, Tools, Prompts`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

### Scenario Playbook 1: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 31: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 32: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 33: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 34: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 35: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 36: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 37: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 38: Chapter 3: Template MCP Primitives: Resources, Tools, Prompts

- tutorial context: **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for core abstractions in this chapter so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Template MCP Primitives: Resources, Tools, Prompts` as an operating subsystem inside **Create TypeScript Server Tutorial: Scaffold MCP Servers with TypeScript Templates**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around execution and reliability details as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Template MCP Primitives: Resources, Tools, Prompts` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `core component`.
2. **Input normalization**: shape incoming data so `execution layer` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `state model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Create TypeScript Server README](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/README.md)
  Why it matters: authoritative reference on `Create TypeScript Server README` (github.com).
- [Template README](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/README.md.ejs)
  Why it matters: authoritative reference on `Template README` (github.com).
- [Template Server Source](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/src/index.ts.ejs)
  Why it matters: authoritative reference on `Template Server Source` (github.com).
- [Template Package Metadata](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/template/package.json.ejs)
  Why it matters: authoritative reference on `Template Package Metadata` (github.com).
- [Contributing Guide](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/CONTRIBUTING.md)
  Why it matters: authoritative reference on `Contributing Guide` (github.com).
- [Security Policy](https://github.com/modelcontextprotocol/create-typescript-server/blob/main/SECURITY.md)
  Why it matters: authoritative reference on `Security Policy` (github.com).

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Generated Structure and Build Pipeline](02-generated-structure-and-build-pipeline.md)
- [Next Chapter: Chapter 4: Configuration, Metadata, and Packaging](04-configuration-metadata-and-packaging.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
