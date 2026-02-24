---
layout: default
title: "Chapter 5: Transports: STDIO and Streamable HTTP"
nav_order: 5
parent: MCP PHP SDK Tutorial
---

# Chapter 5: Transports: STDIO and Streamable HTTP

Welcome to **Chapter 5: Transports: STDIO and Streamable HTTP**. In this part of **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter maps transport choice to runtime and operational constraints.

## Learning Goals

- choose stdio vs streamable HTTP by workload
- understand HTTP method/session behavior requirements
- integrate streamable HTTP into framework middleware stacks
- validate transport behavior with Inspector and curl workflows

## Transport Matrix

| Transport | Best Fit |
|:----------|:---------|
| STDIO | local MCP clients, desktop integrations, subprocess servers |
| Streamable HTTP | web apps, framework routes, distributed services |

## Implementation Notes

- stdio is simplest for local testing and client config bootstrapping.
- HTTP transport requires PSR-17 factories and careful session/header handling.
- framework integrations (Symfony/Laravel/Slim) should wrap transport lifecycle cleanly.

## Source References

- [Transports Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/transports.md)
- [Server Examples README](https://github.com/modelcontextprotocol/php-sdk/blob/main/examples/server/README.md)
- [Examples Guide - Running Examples](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/examples.md#running-examples)

## Summary

You now have a transport selection model for PHP MCP deployment contexts.

Next: [Chapter 6: Client Communication: Sampling, Logging, and Progress](06-client-communication-sampling-logging-and-progress.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- tutorial slug: **mcp-php-sdk-tutorial**
- chapter focus: **Chapter 5: Transports: STDIO and Streamable HTTP**
- system context: **Mcp Php Sdk Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 5: Transports: STDIO and Streamable HTTP`.
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

- [PHP SDK README](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md)
- [PHP SDK Guides Index](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/index.md)
- [Server Builder Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md)
- [MCP Elements Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/mcp-elements.md)
- [Transports Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/transports.md)
- [Client Communication Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-client-communication.md)
- [Examples Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/examples.md)
- [Server Examples README](https://github.com/modelcontextprotocol/php-sdk/blob/main/examples/server/README.md)

### Cross-Tutorial Connection Map

- [MCP Specification Tutorial](../mcp-specification-tutorial/)
- [MCP Python SDK Tutorial](../mcp-python-sdk-tutorial/)
- [MCP TypeScript SDK Tutorial](../mcp-typescript-sdk-tutorial/)
- [MCP Ruby SDK Tutorial](../mcp-ruby-sdk-tutorial/)
- [Chapter 1: Getting Started and Experimental Baseline](01-getting-started-and-experimental-baseline.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 5: Transports: STDIO and Streamable HTTP`.
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

### Scenario Playbook 1: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 31: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 32: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 33: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 34: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 35: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 36: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 37: Chapter 5: Transports: STDIO and Streamable HTTP

- tutorial context: **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**
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

After working through this chapter, you should be able to reason about `Chapter 5: Transports: STDIO and Streamable HTTP` as an operating subsystem inside **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around execution and reliability details as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Transports: STDIO and Streamable HTTP` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `core component`.
2. **Input normalization**: shape incoming data so `execution layer` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `state model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [PHP SDK README](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md)
  Why it matters: authoritative reference on `PHP SDK README` (github.com).
- [PHP SDK Guides Index](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/index.md)
  Why it matters: authoritative reference on `PHP SDK Guides Index` (github.com).
- [Server Builder Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md)
  Why it matters: authoritative reference on `Server Builder Guide` (github.com).
- [MCP Elements Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/mcp-elements.md)
  Why it matters: authoritative reference on `MCP Elements Guide` (github.com).
- [Transports Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/transports.md)
  Why it matters: authoritative reference on `Transports Guide` (github.com).
- [Client Communication Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-client-communication.md)
  Why it matters: authoritative reference on `Client Communication Guide` (github.com).
- [Examples Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/examples.md)
  Why it matters: authoritative reference on `Examples Guide` (github.com).
- [Server Examples README](https://github.com/modelcontextprotocol/php-sdk/blob/main/examples/server/README.md)
  Why it matters: authoritative reference on `Server Examples README` (github.com).

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Discovery, Manual Registration, and Caching](04-discovery-manual-registration-and-caching.md)
- [Next Chapter: Chapter 6: Client Communication: Sampling, Logging, and Progress](06-client-communication-sampling-logging-and-progress.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
