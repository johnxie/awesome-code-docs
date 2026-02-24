---
layout: default
title: "Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks"
nav_order: 5
parent: MCP Rust SDK Tutorial
---

# Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

Welcome to **Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks**. In this part of **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


rmcp supports a wide capability surface; quality comes from selective, coherent implementation.

## Learning Goals

- design tools/resources/prompts with clear contracts
- use task augmentation and task lifecycle APIs safely
- support progress and long-running workflows with predictable semantics
- avoid capability sprawl in one server binary

## Capability Build Order

1. tool/resource/prompt baseline with strict schema contracts
2. progress and logging for observability
3. task support only where long-running execution is required
4. sampling/elicitation for human-in-the-loop workflows

## Source References

- [rmcp README - Tasks](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/README.md#tasks)
- [Server Examples README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/servers/README.md)
- [rmcp Changelog - Task Updates](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/CHANGELOG.md)

## Summary

You now have a staged capability approach for building robust Rust MCP servers.

Next: [Chapter 6: OAuth, Security, and Auth Workflows](06-oauth-security-and-auth-workflows.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- tutorial slug: **mcp-rust-sdk-tutorial**
- chapter focus: **Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks**
- system context: **Mcp Rust Sdk Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks`.
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

- [Rust SDK README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/README.md)
- [rmcp Crate README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/README.md)
- [rmcp-macros README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp-macros/README.md)
- [OAuth Support Guide](https://github.com/modelcontextprotocol/rust-sdk/blob/main/docs/OAUTH_SUPPORT.md)
- [Examples Index](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/README.md)
- [Client Examples](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/clients/README.md)
- [Server Examples](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/servers/README.md)
- [rmcp Changelog](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/CHANGELOG.md)

### Cross-Tutorial Connection Map

- [MCP Specification Tutorial](../mcp-specification-tutorial/)
- [MCP Go SDK Tutorial](../mcp-go-sdk-tutorial/)
- [MCP Java SDK Tutorial](../mcp-java-sdk-tutorial/)
- [MCP Swift SDK Tutorial](../mcp-swift-sdk-tutorial/)
- [Chapter 1: Getting Started and Crate Setup](01-getting-started-and-crate-setup.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks`.
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

### Scenario Playbook 1: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 31: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 32: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 33: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 34: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 35: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 36: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 37: Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks

- tutorial context: **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for core abstractions in this chapter so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks` as an operating subsystem inside **MCP Rust SDK Tutorial: Building High-Performance MCP Services with RMCP**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around execution and reliability details as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Server Patterns: Tools, Resources, Prompts, and Tasks` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `core component`.
2. **Input normalization**: shape incoming data so `execution layer` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `state model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Rust SDK README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/README.md)
  Why it matters: authoritative reference on `Rust SDK README` (github.com).
- [rmcp Crate README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/README.md)
  Why it matters: authoritative reference on `rmcp Crate README` (github.com).
- [rmcp-macros README](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp-macros/README.md)
  Why it matters: authoritative reference on `rmcp-macros README` (github.com).
- [OAuth Support Guide](https://github.com/modelcontextprotocol/rust-sdk/blob/main/docs/OAUTH_SUPPORT.md)
  Why it matters: authoritative reference on `OAuth Support Guide` (github.com).
- [Examples Index](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/README.md)
  Why it matters: authoritative reference on `Examples Index` (github.com).
- [Client Examples](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/clients/README.md)
  Why it matters: authoritative reference on `Client Examples` (github.com).
- [Server Examples](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/servers/README.md)
  Why it matters: authoritative reference on `Server Examples` (github.com).
- [rmcp Changelog](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/CHANGELOG.md)
  Why it matters: authoritative reference on `rmcp Changelog` (github.com).

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Client Patterns, Sampling, and Batching Flows](04-client-patterns-sampling-and-batching-flows.md)
- [Next Chapter: Chapter 6: OAuth, Security, and Auth Workflows](06-oauth-security-and-auth-workflows.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
