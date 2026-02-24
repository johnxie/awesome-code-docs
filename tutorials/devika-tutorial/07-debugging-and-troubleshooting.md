---
layout: default
title: "Chapter 7: Debugging and Troubleshooting"
nav_order: 7
parent: Devika Tutorial
---

# Chapter 7: Debugging and Troubleshooting

Welcome to **Chapter 7: Debugging and Troubleshooting**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter covers how to diagnose and resolve failures in Devika's agent pipeline, from startup errors to mid-task agent loops, using logs, the self-reflection mechanism, and targeted countermeasures.

## Learning Goals

- identify the log sources and log levels that expose agent pipeline state during task execution
- diagnose the most common failure patterns across planner, researcher, coder, and action agents
- understand how the internal monologue self-reflection loop can be leveraged as a debugging signal
- apply systematic countermeasures for each failure category without restarting the entire pipeline

## Fast Start Checklist

1. enable DEBUG log level in config.toml and observe the agent interaction log during a task run
2. submit a task that deliberately requires web research and trace the full researcher log output
3. identify the log line that indicates a coder agent invocation and the line that confirms file write
4. simulate a deliberate error (bad API key) and trace it from the request to the error log entry

## Source References

- [Devika Logs and Debugging](https://github.com/stitionai/devika#debugging)
- [Devika Agent Source](https://github.com/stitionai/devika/tree/main/src/agents)
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Repository](https://github.com/stitionai/devika)

## Summary

You now have a systematic debugging playbook for Devika that covers log interpretation, agent failure diagnosis, and targeted countermeasures for every major failure category in the pipeline.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 7: Debugging and Troubleshooting**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Devika's Python backend emits structured logs via the standard Python `logging` module; log level is configured in `config.toml` under `LOG_LEVEL` and defaults to `INFO`.
2. Each agent logs its invocation with the model used, step context, and a timestamp; setting `LOG_LEVEL=DEBUG` adds full prompt and response payloads to the logs.
3. The orchestrator logs state transitions between agents (planner → researcher → coder → action → monologue) allowing pipeline tracing without code instrumentation.
4. The internal monologue agent logs its decision (`proceed`, `revise`, or `done`) along with the reasoning text; this is the primary signal for diagnosing loop problems.
5. Playwright browser errors are captured by the browser module and logged with the URL, HTTP status, and error message; headless mode errors may require switching to headful for visual debugging.
6. Qdrant connection errors surface as Python `grpc` or `httpx` exceptions in the backend log; they indicate the vector store is unreachable before or during task execution.
7. LLM provider errors (rate limits, auth failures, context overflow) are caught in the `src/llm/` abstraction and logged with the provider name, error code, and request metadata.
8. The action agent logs stdout and stderr from executed code; these logs are the primary signal for diagnosing code correctness issues in generated programs.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Log verbosity | INFO for production | DEBUG for active debugging sessions | disk usage vs diagnostic detail |
| Log storage | stdout only | structured JSON logs to file + log aggregation | simplicity vs searchability |
| Error alerting | manual log review | alert on error patterns via log aggregation tool | operational overhead vs response time |
| Agent replay | re-submit entire task | patch intermediate state and replay from specific step | simplicity vs efficiency |
| Debugging browser issues | headless mode + log analysis | headful Playwright with screenshots on failure | invisibility vs visual clarity |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Backend silent failure | task submitted but no agent log output | unhandled exception in orchestrator before first log line | add a try/except at the orchestrator entry point and log all exceptions |
| Researcher hangs indefinitely | no researcher completion log after 60 seconds | Playwright navigation hangs on a slow-loading page | add Playwright navigation timeout (30 seconds) and fall through to next result URL |
| Coder produces truncated JSON | JSON parse error in orchestrator | coder LLM response was cut off due to context limit | reduce context chunk size or switch to larger context window model |
| Action agent not invoked | task completes but no code was executed | coder returned no `terminal_command` field | verify coder prompt includes instruction to add `terminal_command` when code is executable |
| Internal monologue returns null | orchestrator crashes with NullPointerError | monologue LLM returned malformed JSON | add JSON validation with fallback decision (default to `proceed`) on monologue parse failure |
| Qdrant retrieval returns 0 chunks | coder receives empty research context | Qdrant collection empty or wrong namespace queried | verify researcher upsert succeeded by checking Qdrant dashboard after researcher step |

### Implementation Runbook

1. Set `LOG_LEVEL=DEBUG` in config.toml and restart the backend to enable full prompt/response logging.
2. Submit a failing task and capture the full backend log output to a file: `python devika.py 2>&1 | tee debug.log`.
3. Search the log for the specific agent that last logged before the failure: `grep "AGENT_STEP" debug.log`.
4. For researcher failures, search for `PLAYWRIGHT` and `QDRANT` log lines to trace browser and storage operations.
5. For coder failures, search for `CODER_INVOCATION` and `FILE_WRITE` log lines to verify code generation and file output.
6. For monologue loop issues, search for `MONOLOGUE_DECISION` log lines and count iterations to detect infinite loops.
7. For action agent failures, search for `EXECUTION_STDOUT` and `EXECUTION_STDERR` log lines to read generated code output.
8. For provider errors, search for the provider name and `ERROR` in the log to identify authentication or rate limit failures.
9. After identifying the root cause, apply the targeted countermeasure from the failure modes table and re-submit the task.

### Quality Gate Checklist

- [ ] LOG_LEVEL is configurable at runtime without code changes
- [ ] all agent invocations emit structured log entries with agent name, step number, and model used
- [ ] orchestrator state transitions are logged at INFO level for production tracing
- [ ] Playwright navigation has an explicit timeout configured to prevent indefinite hangs
- [ ] coder JSON response is validated before parsing and malformed responses are logged and retried
- [ ] internal monologue parse failures have a safe fallback decision to prevent orchestrator crash
- [ ] action agent stdout and stderr are captured and logged for every code execution
- [ ] Qdrant retrieval result count is logged per step to detect empty context early

### Source Alignment

- [Devika Agent Source Directory](https://github.com/stitionai/devika/tree/main/src/agents)
- [Devika README Debugging Section](https://github.com/stitionai/devika#debugging)
- [Devika Browser Module](https://github.com/stitionai/devika/tree/main/src/browser)
- [Devika LLM Abstraction](https://github.com/stitionai/devika/tree/main/src/llm)
- [Devika Repository](https://github.com/stitionai/devika)

### Cross-Tutorial Connection Map

- [OpenHands Tutorial](../openhands-tutorial/) — debugging patterns for a comparable autonomous coding agent
- [LangFuse Tutorial](../langfuse-tutorial/) — LLM observability platform applicable to tracing Devika agent calls
- [SWE-agent Tutorial](../swe-agent-tutorial/) — debugging autonomous agent loops in a single-agent architecture
- [Playwright MCP Tutorial](../playwright-mcp-tutorial/) — Playwright-specific debugging and error handling techniques
- [LiteLLM Tutorial](../litellm-tutorial/) — LLM proxy debugging for identifying provider-level issues

### Advanced Practice Exercises

1. Instrument the Devika orchestrator with OpenTelemetry spans for each agent invocation and export traces to Jaeger for visual pipeline tracing.
2. Write a log parser script that reads a Devika debug log and produces a timeline table showing agent invocations, durations, and decisions.
3. Build a "dry run" mode that runs the planner and researcher but skips the coder and action agents, enabling research validation without code generation.
4. Add structured JSON logging to all agent invocations and configure log aggregation in Grafana Loki or similar for searchable multi-task log correlation.
5. Implement an automatic retry-with-backoff mechanism in the orchestrator that re-invokes a failed agent step up to three times before escalating to a task failure.

### Review Questions

1. What log level must be set in config.toml to see full prompt and response payloads in the backend log?
2. What is the primary log signal that indicates the internal monologue agent has entered an infinite revision loop?
3. How do you diagnose whether a Qdrant retrieval is returning empty results versus the researcher failing to upsert chunks?
4. What Playwright configuration change allows you to visually observe browser behavior during a debugging session?
5. What is the safe fallback decision for the orchestrator to take if the internal monologue returns malformed JSON?

### Scenario Playbook 1: Task Submitted But No Agent Log Output

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task is submitted through the UI but the backend log shows no agent invocation lines
- initial hypothesis: unhandled exception in the orchestrator before the first agent is invoked
- immediate action: set LOG_LEVEL=DEBUG and re-submit; look for a stack trace immediately after the task submission log line
- engineering control: wrap the orchestrator entry point in a top-level try/except that logs any exception with full traceback before re-raising
- verification target: any exception in the orchestrator path is logged with full context before the task is marked as failed
- rollback trigger: broad exception catching masks specific errors that need different handling paths
- communication step: document the "silent task failure" symptom and the LOG_LEVEL=DEBUG diagnostic step in the troubleshooting guide
- learning capture: add an integration test that injects a known bad input and asserts that an error log entry is produced

### Scenario Playbook 2: Researcher Hangs on Slow-Loading Page

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task progress stops for 5+ minutes; last log line is from the researcher agent navigating to a URL
- initial hypothesis: Playwright is waiting indefinitely for a slow or unresponsive web page to finish loading
- immediate action: add a 30-second navigation timeout to Playwright's `page.goto()` call and configure `wait_for_load_state` to use `'domcontentloaded'` instead of `'networkidle'`
- engineering control: wrap all Playwright navigation in a try/except for `TimeoutError` that falls through to the next result URL
- verification target: researcher completes all steps within 120 seconds even when individual page loads time out
- rollback trigger: 30-second timeout causes legitimate slow documentation sites to be skipped; increase to 60 seconds
- communication step: document the navigation timeout configuration in the browser module README
- learning capture: add a researcher timeout test that mocks a slow URL and asserts the fallback behavior

### Scenario Playbook 3: Coder Returns Malformed JSON

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: orchestrator crashes with a JSON parse error after the coder agent step
- initial hypothesis: the coder LLM response was truncated due to the context window limit, cutting off the JSON payload
- immediate action: check the coder log for the raw LLM response and identify where the JSON is truncated
- engineering control: add JSON validation with error logging before parsing; implement a retry with a shorter context if parse fails
- verification target: truncated JSON responses trigger a logged retry rather than an orchestrator crash
- rollback trigger: context reduction retry produces lower quality code; flag as a warning and surface to the operator
- communication step: document the JSON truncation failure mode and the context window limit recommendation in the troubleshooting guide
- learning capture: add a coder JSON validation unit test with a known-truncated response fixture

### Scenario Playbook 4: Internal Monologue Loops 15 Times Without Completing

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: agent task runs for 30 minutes with repeated "revise" decisions in the monologue log
- initial hypothesis: the monologue model is hallucinating "not done" because the completion criteria are not clear
- immediate action: inject the iteration count into the monologue prompt with an explicit instruction: "if iteration > 8, return done"
- engineering control: add a hard cap on monologue iterations in the orchestrator; after 10 iterations, force the `done` decision and log a warning
- verification target: no task runs more than 10 monologue iterations on benchmark tasks; tasks complete in under 15 minutes
- rollback trigger: forced completion causes incomplete workspace output on legitimately complex multi-step tasks
- communication step: surface the iteration count in the UI task progress view so users can monitor loop depth
- learning capture: add per-task monologue iteration count as a metric and set an alert at 8 iterations

### Scenario Playbook 5: Action Agent Code Execution Silently Fails

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task completes successfully but running the generated code manually produces errors
- initial hypothesis: the action agent executed the code but swallowed the non-zero exit code without logging it
- immediate action: add explicit return code checking in the action agent: log stderr and raise if exit code is non-zero
- engineering control: surface action agent exit codes and stderr in the UI task result view for operator review
- verification target: any non-zero exit code from code execution appears in the backend log and the task result
- rollback trigger: strict exit code checking causes task failure on warnings that don't affect functionality
- communication step: document the code execution error visibility feature in the user guide
- learning capture: add an action agent test that runs code with a known error and asserts the exit code is logged

### What Problem Does This Solve?

Devika's multi-agent pipeline creates multiple potential failure points that are invisible without structured debugging. A task that "completes" may have silently skipped research, generated truncated code, or looped without producing real output. Without systematic log analysis and targeted countermeasures for each agent boundary, engineers waste significant time re-submitting tasks and guessing at root causes. This chapter provides the diagnostic toolset that converts opaque pipeline failures into actionable, repeatable debugging workflows.

### How it Works Under the Hood

1. The Python backend uses the `logging` module with configurable handlers; at DEBUG level, each agent logs its full prompt and LLM response.
2. The orchestrator logs a state transition entry at each agent handoff, creating a breadcrumb trail through the pipeline.
3. Playwright errors are caught as Python exceptions in the browser module and logged with URL, status, and error type.
4. LLM provider errors are caught in the `src/llm/` abstraction and re-raised as typed exceptions that the orchestrator can handle distinctly.
5. The internal monologue decision is logged as a structured JSON entry with the decision type and the reasoning text.
6. Action agent execution uses Python's `subprocess` module; stdout and stderr are captured and logged regardless of exit code.

### Source Walkthrough

- [Devika Agent Source Directory](https://github.com/stitionai/devika/tree/main/src/agents) — Why it matters: the implementation of each agent including logging, error handling, and LLM invocation.
- [Devika LLM Abstraction](https://github.com/stitionai/devika/tree/main/src/llm) — Why it matters: the provider error handling layer where rate limits, auth failures, and truncation errors are caught.
- [Devika Browser Module](https://github.com/stitionai/devika/tree/main/src/browser) — Why it matters: the Playwright integration including navigation, content extraction, and error handling code.
- [Devika README Debugging](https://github.com/stitionai/devika#debugging) — Why it matters: the official guidance on log level configuration and debugging procedures.

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Project Management and Workspaces](06-project-management-and-workspaces.md)
- [Next Chapter: Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
