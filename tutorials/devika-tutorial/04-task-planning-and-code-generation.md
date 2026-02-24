---
layout: default
title: "Chapter 4: Task Planning and Code Generation"
nav_order: 4
parent: Devika Tutorial
---

# Chapter 4: Task Planning and Code Generation

Welcome to **Chapter 4: Task Planning and Code Generation**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter explains how Devika's planner agent decomposes a user prompt into an executable step plan, and how the coder agent transforms each step plus research context into production-ready code files.

## Learning Goals

- understand how the planner agent structures a task into numbered steps with dependencies
- trace how each plan step becomes a coder agent invocation with a bounded context
- identify prompt engineering patterns that improve planning quality and code generation accuracy
- recognize failure modes in task decomposition and apply countermeasures

## Fast Start Checklist

1. submit a small, well-scoped coding task and observe the plan output in the agent log
2. examine the coder prompt template to see how plan steps and research context are assembled
3. review the generated workspace files to verify step-to-file correspondence
4. experiment with prompt phrasing to observe its effect on step count and code quality

## Source References

- [Devika Planner Agent Source](https://github.com/stitionai/devika/tree/main/src/agents/planner)
- [Devika Coder Agent Source](https://github.com/stitionai/devika/tree/main/src/agents/coder)
- [Devika How It Works](https://github.com/stitionai/devika#how-it-works)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)

## Summary

You now understand how Devika converts a natural language task into a structured execution plan and how each plan step drives a focused code generation call with research-enriched context.

Next: [Chapter 5: Web Research and Browser Integration](05-web-research-and-browser-integration.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 4: Task Planning and Code Generation**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. The planner agent receives the raw user prompt and the project context (existing files, previous steps) and returns a JSON array of step objects, each with a `step_number`, `task`, and optional `search_query` field.
2. Steps with a `search_query` field are routed to the researcher agent before the coder agent is invoked for that step; steps without search queries go directly to the coder.
3. The coder agent prompt assembles three context blocks: (a) the current step description, (b) Qdrant-retrieved research chunks for this step, and (c) a file tree snapshot of the current workspace.
4. The coder agent returns a JSON object with a `code` block, a `file_name`, and an optional `terminal_command` for execution by the action agent.
5. File names returned by the coder agent are relative to the project workspace root; the orchestrator writes each file using the returned path.
6. When a step requires modifying an existing file, the coder receives the current file content in its context window; the returned code replaces the entire file.
7. The planner can emit a `done` flag on the last step to signal the orchestrator to terminate rather than entering another monologue revision loop.
8. Prompt clarity in the user's task description directly controls planner step granularity; vague prompts produce vague steps and lower-quality code generation.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Task prompt granularity | single high-level prompt | multi-sentence prompt with tech stack and constraints | ease of use vs output precision |
| Plan step count | LLM-default decomposition | instruct model to limit to N steps | flexibility vs token budget |
| Code file granularity | let coder decide file structure | specify expected file names in the task prompt | autonomy vs predictability |
| Existing code context | no existing code provided | paste existing code snippets into the task prompt | speed vs contextual accuracy |
| Iterative refinement | submit new task per revision | use internal monologue loop for in-session revision | simplicity vs session continuity |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Planner produces duplicate steps | two steps with identical task descriptions | ambiguous prompt allows LLM to repeat itself | add deduplication validation on planner output before dispatching |
| Coder generates code for wrong language | Python output for a JavaScript task | task prompt did not specify language; researcher found Python examples | add explicit language constraint in task prompt and planner system prompt |
| Generated code has syntax errors | action agent execution fails with SyntaxError | coder truncated output due to context window limit | reduce context chunk size or switch to a larger context window model |
| Missing import statements | code runs but NameError at runtime | coder generated function bodies without headers | add a "always include all imports" instruction to the coder system prompt |
| Wrong file path from coder | file written to wrong workspace location | coder returns absolute path instead of relative path | validate and normalize returned file_name to be workspace-relative before writing |
| Step dependencies not respected | step N uses variable defined in step N+2 | planner did not model data dependencies between steps | instruct planner to annotate each step with its dependencies in the step JSON |

### Implementation Runbook

1. Write a clear task prompt that specifies language, framework, expected output structure, and any constraints.
2. Submit the task and observe the planner output in the backend logs to verify step decomposition quality.
3. For each step in the plan, verify whether a `search_query` is present and whether it accurately captures what research is needed.
4. After each coder invocation, verify the workspace file matches the expected step output before the next step proceeds.
5. If code quality is low, experiment with adding explicit constraints to the user prompt (e.g., "write type-annotated Python 3.10 with pytest unit tests").
6. For complex multi-file projects, seed the task prompt with the expected project structure to guide coder file naming.
7. Monitor the internal monologue logs to verify the agent correctly identifies when each step is complete.
8. After task completion, review all workspace files for completeness, correct imports, and integration consistency across files.
9. Run the generated code locally or in the action agent's execution environment to validate correctness before using in production.

### Quality Gate Checklist

- [ ] task prompts include language, framework, and constraint specifications to guide the planner
- [ ] planner output is validated for step completeness and absence of duplicate or contradictory steps
- [ ] each coder invocation receives the correct research context chunks for its step
- [ ] generated code files are written to correct workspace-relative paths
- [ ] all generated files include necessary imports and dependency declarations
- [ ] action agent execution results are surfaced to the orchestrator for error detection
- [ ] internal monologue correctly identifies task completion vs. continued revision need
- [ ] final workspace is reviewed for cross-file integration consistency

### Source Alignment

- [Devika Planner Agent](https://github.com/stitionai/devika/tree/main/src/agents/planner)
- [Devika Coder Agent](https://github.com/stitionai/devika/tree/main/src/agents/coder)
- [Devika How It Works](https://github.com/stitionai/devika#how-it-works)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika Prompts Directory](https://github.com/stitionai/devika/tree/main/prompts)

### Cross-Tutorial Connection Map

- [DSPy Tutorial](../dspy-tutorial/) — systematic prompt optimization techniques applicable to Devika's planner prompts
- [LangGraph Tutorial](../langgraph-tutorial/) — graph-based task decomposition for comparison with Devika's linear plan
- [CrewAI Tutorial](../crewai-tutorial/) — role-based task assignment patterns in multi-agent coding systems
- [Aider Tutorial](../aider-tutorial/) — simpler code generation workflow for baseline quality comparison
- [OpenHands Tutorial](../openhands-tutorial/) — alternative multi-agent coding system with different planning approach

### Advanced Practice Exercises

1. Write five different task prompts for the same coding problem at different specificity levels and compare the planner step outputs and final code quality.
2. Modify the planner prompt template to add a `dependencies` field to each step and verify the orchestrator respects the dependency ordering.
3. Add a plan validation function that checks for duplicate step descriptions and orphaned `search_query` fields before dispatching to the researcher.
4. Instrument the coder agent to log the exact assembled prompt (with research context) for each step and analyze token usage per step.
5. Build a post-processing script that runs `pylint` or `eslint` on all coder-generated files and reports quality scores per task.

### Review Questions

1. What fields does a planner step JSON object contain and which field controls whether the researcher agent is invoked for that step?
2. What three context blocks are assembled into the coder agent prompt and what is the source of each?
3. How does the coder agent return file content to the orchestrator and how does the orchestrator determine where to write each file?
4. What prompt engineering techniques most reliably improve planner step granularity and code quality?
5. What failure mode occurs when the coder agent's output is truncated due to a context window limit and how do you detect it?

### Scenario Playbook 1: Task Prompt Too Vague Produces Poor Plan

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: user submits "build me a web app" and the planner returns only 2 generic steps
- initial hypothesis: the prompt lacks specificity about language, framework, features, and output structure
- immediate action: revise the prompt to include technology stack, feature list, and expected file structure
- engineering control: add a prompt quality guide to the UI that prompts users to specify language, framework, and constraints before submission
- verification target: revised prompt produces a plan with 5-8 specific, actionable steps with accurate search queries
- rollback trigger: detailed prompt still produces generic plan; investigate planner prompt template for missing instruction
- communication step: publish a task prompt writing guide with good and bad examples in the team knowledge base
- learning capture: add prompt quality scoring to the pre-submission flow that warns when key specificity signals are absent

### Scenario Playbook 2: Coder Generates Python Instead of TypeScript

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task requested a TypeScript Node.js API but coder produces Python Flask code
- initial hypothesis: researcher found Python examples that dominated the Qdrant context, biasing the coder
- immediate action: re-submit with explicit "TypeScript" and "Node.js" in both the task prompt and as a constraint
- engineering control: inject a language constraint into the planner system prompt so each plan step carries the target language
- verification target: coder generates `.ts` files with TypeScript syntax for all subsequent tasks specifying TypeScript
- rollback trigger: language constraint causes coder to ignore research context that only has Python examples
- communication step: add language specification to the task prompt template shown in the UI
- learning capture: add a file extension validation post-step that alerts if generated files don't match the specified language

### Scenario Playbook 3: Generated Code Has Missing Imports

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: action agent execution fails with `NameError: name 'requests' is not defined` on generated code
- initial hypothesis: coder generated function bodies without including the `import requests` header
- immediate action: manually add the import and re-execute; inspect the coder prompt template for import instructions
- engineering control: add "always include all import statements at the top of every generated file" to the coder system prompt
- verification target: subsequent code generation includes complete import blocks for all symbols used in the function body
- rollback trigger: import instruction causes hallucinated imports for libraries not actually used
- communication step: document the import completeness requirement in the code generation quality standards
- learning capture: add a static import checker as a post-step validation that flags missing imports before action agent execution

### Scenario Playbook 4: Planner Steps Exceed Context Budget

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: a complex task generates 15 steps; mid-task coder calls fail with context overflow
- initial hypothesis: accumulated plan + research context + workspace snapshot exceeds the model's context window
- immediate action: limit the workspace snapshot to the most recently modified files rather than the full file tree
- engineering control: add a context budget manager that trims the workspace snapshot to fit within the available token budget
- verification target: no context overflow errors for tasks up to 15 steps with moderate research context
- rollback trigger: workspace snapshot trimming causes the coder to generate conflicting code that overwrites earlier work
- communication step: document the context window budget model and recommended max step count per model size
- learning capture: add per-step token usage logging to identify which context blocks consume the most budget

### Scenario Playbook 5: Multi-File Project Has Integration Inconsistencies

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task generates 5 files but function names in `main.py` don't match those defined in `utils.py`
- initial hypothesis: each coder invocation is independent and does not read previously generated files
- immediate action: verify whether the workspace file tree snapshot is injected into the coder context for each step
- engineering control: ensure the full content of all previously generated files is included in the coder context for each subsequent step
- verification target: coder references correct function signatures from earlier-generated files in all integration points
- rollback trigger: including all file contents exceeds context window; use summarized file interfaces instead of full content
- communication step: document the cross-file context injection strategy in the architecture guide
- learning capture: add an integration consistency test that checks import/export symbol names across all generated files

### What Problem Does This Solve?

Devika's task planning and code generation pipeline solves the coherence problem in autonomous code generation. Without a structured plan, an LLM asked to build a multi-file application tends to generate incomplete or internally inconsistent code in a single shot. By decomposing the task into sequential steps with bounded context at each step, Devika produces code that is incrementally verifiable, traceable to specific plan steps, and enriched with web-researched context that the LLM would not have had in its training data.

### How it Works Under the Hood

1. The user prompt is sent to the planner agent which assembles a system prompt from `prompts/planner/` and produces a JSON step array.
2. The orchestrator iterates over each step; if a `search_query` is present, it dispatches to the researcher agent first.
3. Research results are stored in Qdrant with the task and step as metadata; the coder retrieves them via semantic search.
4. The coder prompt is assembled from the step description, retrieved Qdrant chunks, and the current workspace file tree.
5. The coder returns a JSON object with `file_name`, `code`, and optionally `terminal_command`.
6. The orchestrator writes the file to disk and optionally invokes the action agent to execute the terminal command.

### Source Walkthrough

- [Devika Planner Source](https://github.com/stitionai/devika/tree/main/src/agents/planner) — Why it matters: the implementation of step decomposition and the prompt template that drives plan quality.
- [Devika Coder Source](https://github.com/stitionai/devika/tree/main/src/agents/coder) — Why it matters: the code generation logic including context assembly and file output formatting.
- [Devika Prompts Directory](https://github.com/stitionai/devika/tree/main/prompts) — Why it matters: all prompt templates that can be tuned to improve planning and code generation quality.
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md) — Why it matters: the canonical description of how plan steps drive the coder invocation sequence.

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: LLM Provider Configuration](03-llm-provider-configuration.md)
- [Next Chapter: Chapter 5: Web Research and Browser Integration](05-web-research-and-browser-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 4: Task Planning and Code Generation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
