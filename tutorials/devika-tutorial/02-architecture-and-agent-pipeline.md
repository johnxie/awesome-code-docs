---
layout: default
title: "Chapter 2: Architecture and Agent Pipeline"
nav_order: 2
parent: Devika Tutorial
---

# Chapter 2: Architecture and Agent Pipeline

Welcome to **Chapter 2: Architecture and Agent Pipeline**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter explains how Devika's five specialized agents — planner, researcher, coder, action, and internal monologue — coordinate to transform a single user prompt into working code.

## Learning Goals

- understand the roles and responsibilities of each specialized agent in the Devika pipeline
- trace the data and control flow from task submission through to workspace output
- identify how the internal monologue loop drives iterative self-correction
- reason about the architectural boundaries between agents for debugging and extension

## Fast Start Checklist

1. read the architecture overview in the Devika README and docs directory
2. identify the five agent types and their input/output contracts
3. trace a single task through the pipeline by reading the orchestrator source
4. inspect agent log output for a real task to observe the coordination sequence

## Source References

- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika How It Works](https://github.com/stitionai/devika#how-it-works)
- [Devika Agent Source](https://github.com/stitionai/devika/tree/main/src/agents)
- [Devika Repository](https://github.com/stitionai/devika)

## Summary

You now understand how Devika's multi-agent architecture decomposes a high-level task into research, planning, coding, and self-reflection steps that loop until the task is complete.

Next: [Chapter 3: LLM Provider Configuration](03-llm-provider-configuration.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 2: Architecture and Agent Pipeline**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. The **Planner Agent** receives the raw user prompt and decomposes it into a numbered step-by-step execution plan; this plan is the primary control signal for all downstream agents.
2. The **Researcher Agent** takes each planning step and formulates search queries, invokes Playwright to browse the web, and stores retrieved knowledge in Qdrant for semantic recall.
3. The **Coder Agent** receives the plan plus all research context from Qdrant and generates code for each step, writing files to the project workspace.
4. The **Action Agent** executes generated code in the workspace environment, captures stdout/stderr, and returns execution results back into the agent loop.
5. The **Internal Monologue Agent** receives the full context — plan, code, execution result — and produces a self-reflection decision: proceed to the next step, revise the current step, or mark the task complete.
6. The orchestrator in `devika.py` manages the loop state machine, routing between agents based on internal monologue output until a terminal condition is reached.
7. All inter-agent communication passes through structured JSON payloads with defined schemas; the LLM prompt templates are versioned in the `prompts/` directory.
8. Qdrant stores embeddings of all research artifacts and previously generated code snippets, enabling the coder agent to reference earlier findings without re-searching.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Max loop iterations | default unbounded loop | explicit max_iterations cap in config | simplicity vs runaway cost |
| Research depth | shallow single-page research | deep multi-page crawl with Playwright | speed vs research completeness |
| Code execution sandbox | run in local workspace | Docker-isolated execution environment | setup simplicity vs blast radius |
| Internal monologue model | same model as coder | cheaper fast model for monologue only | cost savings vs reflection quality |
| Step plan granularity | LLM-default decomposition | inject custom plan prefix to control step count | flexibility vs predictability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Infinite planning loop | task never reaches coder agent | planner keeps revising plan without progressing | add max_iterations guard and force-advance after threshold |
| Research context overflow | coder agent receives truncated context | Qdrant retrieval returns too many chunks | tune top-k retrieval parameter and add context window budget |
| Coder ignores research | generated code doesn't use fetched libraries | researcher output not injected into coder prompt | verify prompt template includes `{research_context}` variable |
| Action agent silent failure | task completes but workspace is empty | code execution error swallowed without logging | add explicit error capture in action agent and surface in UI |
| Internal monologue loop | agent cycles without progress | monologue model hallucinates "not done" indefinitely | inject step counter into monologue prompt; enforce done after N retries |
| Cross-agent state corruption | later agent uses stale data from previous task | session context not cleared between tasks | enforce session isolation and clear Qdrant session namespace per task |

### Implementation Runbook

1. Read `src/agents/planner/planner.py` to understand how the plan is constructed from the user prompt.
2. Read `src/agents/researcher/researcher.py` to trace how search queries are generated and how Playwright is invoked.
3. Read `src/agents/coder/coder.py` to see how research context is retrieved from Qdrant and injected into the code generation prompt.
4. Read `src/agents/action/action.py` to understand how generated code is executed and results are captured.
5. Read `src/agents/internal_monologue/internal_monologue.py` to see the self-reflection decision logic.
6. Trace the orchestrator loop in `devika.py` to map the state transitions between agents.
7. Enable debug logging and submit a simple task; compare the logged agent sequences with your architecture map.
8. Identify the prompt templates in `prompts/` that correspond to each agent and note how context variables are injected.
9. Add a custom logging hook at the orchestrator level to emit per-step timing metrics for performance analysis.

### Quality Gate Checklist

- [ ] all five agent types are identified with their input and output contracts documented
- [ ] the orchestrator state machine transitions are mapped for both success and failure paths
- [ ] Qdrant retrieval parameters (top-k, score threshold) are explicitly configured
- [ ] prompt templates for each agent are reviewed and `{variable}` injection points are validated
- [ ] max_iterations or equivalent loop guard is set to prevent runaway execution
- [ ] inter-agent JSON schema is validated against actual message payloads in logs
- [ ] code execution in the action agent has explicit error capture and surface-to-UI reporting
- [ ] session isolation ensures no cross-task context bleed in Qdrant namespaces

### Source Alignment

- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika How It Works Section](https://github.com/stitionai/devika#how-it-works)
- [Devika Agents Source Directory](https://github.com/stitionai/devika/tree/main/src/agents)
- [Devika Prompts Directory](https://github.com/stitionai/devika/tree/main/prompts)
- [Devika Main Orchestrator](https://github.com/stitionai/devika/blob/main/devika.py)

### Cross-Tutorial Connection Map

- [OpenHands Tutorial](../openhands-tutorial/) — comparable multi-agent architecture with different agent role definitions
- [LangGraph Tutorial](../langgraph-tutorial/) — graph-based orchestration model for understanding state machine design
- [CrewAI Tutorial](../crewai-tutorial/) — crew-based multi-agent coordination patterns
- [AutoGen Tutorial](../autogen-tutorial/) — conversational multi-agent framework for comparison
- [SWE-agent Tutorial](../swe-agent-tutorial/) — single-agent loop architecture for contrast with Devika's multi-agent design

### Advanced Practice Exercises

1. Draw the complete state machine for the Devika orchestrator loop including all terminal conditions and retry paths.
2. Add a custom agent role (e.g., a "reviewer" agent) to the pipeline by extending the orchestrator loop and creating a new prompt template.
3. Instrument each agent with a timing decorator and produce a per-step latency breakdown for a representative task.
4. Replace the Qdrant retriever in the researcher agent with a different vector store and verify the coder agent still receives correct context.
5. Write a unit test for the internal monologue agent that injects known context and asserts the correct "proceed/revise/complete" decision.

### Review Questions

1. In what order are the five agents invoked for a typical task, and what triggers each transition?
2. How does the internal monologue agent decide whether to mark a task complete or loop back to revision?
3. What role does Qdrant play in the pipeline, and which agents read from and write to it?
4. How are research artifacts from the researcher agent made available to the coder agent?
5. What is the mechanism that prevents the orchestrator loop from running indefinitely on an ambiguous task?

### Scenario Playbook 1: Planner Produces Overly Long Step List

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task with a broad prompt generates 20+ steps causing excessive token usage
- initial hypothesis: planner prompt does not constrain step count for the given task scope
- immediate action: inspect the planner prompt template and add a max-steps constraint instruction
- engineering control: inject "produce at most 8 steps" into the planner system prompt for standard tasks
- verification target: planner output for comparable prompts stays at 5-8 steps consistently
- rollback trigger: step count reduction causes coder agent to skip critical implementation details
- communication step: document the step count tuning parameter in the operator configuration guide
- learning capture: add step count as an observable metric and alert when it exceeds configured threshold

### Scenario Playbook 2: Coder Agent Ignores Researcher Output

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: generated code does not use any of the libraries or APIs found by the researcher
- initial hypothesis: the research context variable is not being injected into the coder prompt template
- immediate action: print the fully assembled coder prompt to logs and verify the research block is present
- engineering control: add an assertion in the coder agent that raises if research_context is empty when researcher ran
- verification target: coder agent logs show "using N research chunks" for every task where researcher was invoked
- rollback trigger: assertion fails on tasks where research legitimately produced no useful results
- communication step: add a debug flag to the UI that displays which research chunks the coder used
- learning capture: add a researcher-to-coder context injection integration test to the test suite

### Scenario Playbook 3: Internal Monologue Loop Cycles Without Progress

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task stays in revision loop for more than 10 iterations without reaching completion
- initial hypothesis: monologue model is hallucinating "not done" even when all steps are complete
- immediate action: inspect monologue logs to see the specific reason it keeps returning "revise"
- engineering control: inject a step counter and iteration count into the monologue prompt; add "if iteration > 8, mark done" instruction
- verification target: tasks complete within 8 loop iterations for representative benchmarks
- rollback trigger: forced completion causes the coder to produce incomplete output on genuinely multi-step tasks
- communication step: surface the iteration count in the UI so users can see agent progress
- learning capture: capture monologue decision reasons in structured logs for offline pattern analysis

### Scenario Playbook 4: Action Agent Swallows Execution Error

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task reports success but workspace files are incomplete or malformed
- initial hypothesis: the action agent executed code that raised an exception but did not propagate the error to the orchestrator
- immediate action: review action agent error handling code and check if exceptions are caught and discarded
- engineering control: add explicit try/except with structured error return in the action agent; surface stderr in the UI
- verification target: any code execution failure causes the orchestrator to retry or escalate rather than silently proceeding
- rollback trigger: surfacing all errors causes false-positive failure reports on harmless warnings
- communication step: add stderr output to the task detail view in the UI for operator visibility
- learning capture: add a test that injects a known-bad code snippet and asserts the error is reported to the orchestrator

### Scenario Playbook 5: Cross-Task Context Bleed in Qdrant

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: a new task retrieves research artifacts from a previous unrelated task
- initial hypothesis: Qdrant collection is shared across all tasks without namespace isolation
- immediate action: review how the researcher agent writes to and reads from Qdrant and identify the collection or namespace key
- engineering control: prefix all Qdrant operations with the task_id or project_id to create logical namespace isolation
- verification target: researcher agent only retrieves chunks tagged with the current task_id
- rollback trigger: namespace isolation causes performance regression due to smaller retrieval sets
- communication step: document the Qdrant namespace convention in the architecture guide
- learning capture: add a Qdrant isolation test that asserts zero cross-task retrieval after namespace fix

### What Problem Does This Solve?

Devika's multi-agent architecture solves the single-agent context window and capability ceiling problem. A single LLM asked to research, plan, code, execute, and self-reflect within one prompt quickly runs out of context or produces shallow work in each dimension. By separating these concerns into specialized agents, each with a focused prompt and defined input/output contract, Devika achieves higher quality research, more structured planning, and more reliable code generation than a monolithic approach. The internal monologue loop adds iterative self-correction without requiring human intervention at each step.

### How it Works Under the Hood

1. The user submits a task prompt through the frontend; it is stored in SQLite and dispatched to the orchestrator.
2. The orchestrator invokes the planner agent with the raw prompt; the planner returns a structured JSON step list.
3. For each step, the orchestrator invokes the researcher agent with the step description; Playwright fetches web content and Qdrant stores embeddings.
4. The orchestrator invokes the coder agent with the step description plus retrieved Qdrant context; the coder writes files to the workspace.
5. The action agent executes any runnable code and returns stdout/stderr to the orchestrator.
6. The internal monologue agent receives the full context and returns a decision JSON; the orchestrator advances, retries, or terminates based on this decision.

### Source Walkthrough

- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md) — Why it matters: the official architecture diagram and agent role descriptions.
- [Devika How It Works](https://github.com/stitionai/devika#how-it-works) — Why it matters: the high-level narrative of the full pipeline in the README.
- [Devika Agents Directory](https://github.com/stitionai/devika/tree/main/src/agents) — Why it matters: the source of truth for each agent's implementation and prompt assembly.
- [Devika Prompts Directory](https://github.com/stitionai/devika/tree/main/prompts) — Why it matters: the prompt templates that define each agent's behavior and context injection points.

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started](01-getting-started.md)
- [Next Chapter: Chapter 3: LLM Provider Configuration](03-llm-provider-configuration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 2: Architecture and Agent Pipeline

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
