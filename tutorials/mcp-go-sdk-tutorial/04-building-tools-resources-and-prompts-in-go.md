---
layout: default
title: "Chapter 4: Building Tools, Resources, and Prompts in Go"
nav_order: 4
parent: MCP Go SDK Tutorial
---

# Chapter 4: Building Tools, Resources, and Prompts in Go

Welcome to **Chapter 4: Building Tools, Resources, and Prompts in Go**. In this part of **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter shows how to structure server capability handlers with stable contracts.

## Learning Goals

- add tools/resources/prompts with schema-aware handlers
- implement handler behavior that is easy for clients to reason about
- support list-changed notifications and pagination intentionally
- separate tool execution errors from protocol errors

## Server Capability Build Order

1. create `mcp.NewServer` with explicit implementation metadata
2. add one primitive at a time (`AddTool`, `AddResource`, `AddPrompt`)
3. validate input/output schemas at the handler boundary
4. add completion/logging handlers only when needed

## Handler Quality Rules

- keep tool names and descriptions unambiguous
- return structured output when possible
- ensure resource URI patterns are deterministic
- only advertise capabilities that are truly implemented

## Source References

- [Server Features](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/server.md)
- [Sequential Thinking Server Example](https://github.com/modelcontextprotocol/go-sdk/blob/main/examples/server/sequentialthinking/README.md)
- [pkg.go.dev - Server AddTool](https://pkg.go.dev/github.com/modelcontextprotocol/go-sdk/mcp#AddTool)

## Summary

You now have a repeatable way to build server primitives that stay understandable and robust under client load.

Next: [Chapter 5: Client Capabilities: Roots, Sampling, and Elicitation](05-client-capabilities-roots-sampling-and-elicitation.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- tutorial slug: **mcp-go-sdk-tutorial**
- chapter focus: **Chapter 4: Building Tools, Resources, and Prompts in Go**
- system context: **Mcp Go Sdk Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 4: Building Tools, Resources, and Prompts in Go`.
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

- [Go SDK README](https://github.com/modelcontextprotocol/go-sdk/blob/main/README.md)
- [Features Index](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/README.md)
- [Protocol Support](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/protocol.md)
- [Server Features](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/server.md)
- [Client Features](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/client.md)
- [Troubleshooting](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/troubleshooting.md)
- [Rough Edges](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/rough_edges.md)
- [Server Conformance Script](https://github.com/modelcontextprotocol/go-sdk/blob/main/scripts/server-conformance.sh)

### Cross-Tutorial Connection Map

- [MCP Specification Tutorial](../mcp-specification-tutorial/)
- [MCP Python SDK Tutorial](../mcp-python-sdk-tutorial/)
- [MCP TypeScript SDK Tutorial](../mcp-typescript-sdk-tutorial/)
- [FastMCP Tutorial](../fastmcp-tutorial/)
- [Chapter 1: Getting Started and SDK Package Map](01-getting-started-and-sdk-package-map.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 4: Building Tools, Resources, and Prompts in Go`.
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

### Scenario Playbook 1: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 31: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 32: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 33: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 34: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 35: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 36: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 37: Chapter 4: Building Tools, Resources, and Prompts in Go

- tutorial context: **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**
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

After working through this chapter, you should be able to reason about `Chapter 4: Building Tools, Resources, and Prompts in Go` as an operating subsystem inside **MCP Go SDK Tutorial: Building Robust MCP Clients and Servers in Go**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around execution and reliability details as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Building Tools, Resources, and Prompts in Go` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `core component`.
2. **Input normalization**: shape incoming data so `execution layer` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `state model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Go SDK README](https://github.com/modelcontextprotocol/go-sdk/blob/main/README.md)
  Why it matters: authoritative reference on `Go SDK README` (github.com).
- [Features Index](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/README.md)
  Why it matters: authoritative reference on `Features Index` (github.com).
- [Protocol Support](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/protocol.md)
  Why it matters: authoritative reference on `Protocol Support` (github.com).
- [Server Features](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/server.md)
  Why it matters: authoritative reference on `Server Features` (github.com).
- [Client Features](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/client.md)
  Why it matters: authoritative reference on `Client Features` (github.com).
- [Troubleshooting](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/troubleshooting.md)
  Why it matters: authoritative reference on `Troubleshooting` (github.com).
- [Rough Edges](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/rough_edges.md)
  Why it matters: authoritative reference on `Rough Edges` (github.com).
- [Server Conformance Script](https://github.com/modelcontextprotocol/go-sdk/blob/main/scripts/server-conformance.sh)
  Why it matters: authoritative reference on `Server Conformance Script` (github.com).

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Transports: stdio, Streamable HTTP, and Custom Flows](03-transports-stdio-streamable-http-and-custom-flows.md)
- [Next Chapter: Chapter 5: Client Capabilities: Roots, Sampling, and Elicitation](05-client-capabilities-roots-sampling-and-elicitation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
