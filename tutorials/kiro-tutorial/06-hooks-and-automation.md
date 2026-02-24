---
layout: default
title: "Chapter 6: Hooks and Automation"
nav_order: 6
parent: Kiro Tutorial
---

# Chapter 6: Hooks and Automation

Welcome to **Chapter 6: Hooks and Automation**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Kiro hooks are event-driven triggers that invoke agent actions automatically when specific events occur in the workspace. This chapter teaches you how to build hooks that eliminate repetitive manual workflows.

## Learning Goals

- understand the Kiro hook model: events, conditions, and agent actions
- create hooks for common events: file save, test completion, and spec changes
- configure hook conditions to avoid unnecessary agent activations
- combine hooks with steering files for governed automation
- avoid common hook pitfalls like infinite loops and excessive token consumption

## Fast Start Checklist

1. create `.kiro/hooks/` directory in your project root
2. create your first hook file (e.g., `on-save-lint.md`)
3. define the event trigger, condition, and agent action in the hook
4. save a file to trigger the hook and observe the agent response
5. review the hook's agent activity log and refine the condition

## The Hook Model

Each Kiro hook is a markdown file in `.kiro/hooks/` with three components:

| Component | Purpose | Example |
|:----------|:--------|:--------|
| event | what triggers the hook | `file:save`, `test:complete`, `spec:updated` |
| condition | when to activate (optional filter) | `file matches "src/**/*.ts"` |
| action | what the agent does when triggered | "run the linter on the saved file and fix any warnings" |

## Hook File Format

```markdown
---
event: file:save
condition: file matches "src/**/*.ts"
---

# On TypeScript File Save: Run Lint and Format

When a TypeScript file in `src/` is saved, run ESLint with the `--fix` flag on the saved file
and apply Prettier formatting. Report any errors that cannot be auto-fixed.
```

## Built-in Event Types

| Event | Trigger Condition |
|:------|:-----------------|
| `file:save` | any file is saved in the workspace |
| `file:create` | a new file is created |
| `file:delete` | a file is deleted |
| `test:complete` | a test run finishes (pass or fail) |
| `spec:updated` | a file in `.kiro/specs/` is changed |
| `task:complete` | an autonomous agent task completes |
| `git:commit` | a git commit is made in the workspace |
| `chat:response` | the agent produces a chat response |

## Example Hooks

### Auto-Lint on Save

```markdown
---
event: file:save
condition: file matches "src/**/*.{ts,tsx}"
---

# Auto-Lint TypeScript on Save

Run ESLint with `--fix` on the saved file. If there are unfixable errors, open the Problems
panel and highlight the first error. Do not modify files other than the one that was saved.
```

### Test Failure Analysis

```markdown
---
event: test:complete
condition: test_result == "fail"
---

# Analyze Test Failures

When the test run completes with failures, analyze the failing test output and provide:
1. A one-line root cause summary for each failing test
2. The most likely file to fix
3. A suggested code change (do not apply automatically; show in chat)
```

### Spec Update Propagation

```markdown
---
event: spec:updated
condition: file matches ".kiro/specs/**/requirements.md"
---

# Requirements Changed: Check Design Alignment

When requirements.md is updated, review the current design.md for the same spec and
identify any requirements that are not covered by the existing design. List the gaps
in the chat panel without modifying design.md automatically.
```

### Post-Commit Documentation Update

```markdown
---
event: git:commit
condition: commit_files include "src/api/**"
---

# Update API Documentation After API Commit

When a commit modifies files in `src/api/`, check whether `docs/api.md` needs to be
updated to reflect the changes. If documentation is stale, list the specific sections
that need updating in the chat panel.
```

### Task Completion Summary

```markdown
---
event: task:complete
---

# Task Completion: Generate Summary

When an autonomous agent task completes, generate a two-sentence summary of what was
changed, which files were modified, and whether all tests are passing. Log the summary
in `.kiro/task-log.md`.
```

## Condition Syntax

Hook conditions filter when the hook activates. Supported condition expressions:

```
# File pattern matching
file matches "src/**/*.ts"
file matches "*.test.ts"
file not matches "node_modules/**"

# Test result conditions
test_result == "fail"
test_result == "pass"
test_count > 0

# Git conditions
commit_files include "src/api/**"
commit_message contains "feat:"

# Logical operators
file matches "src/**/*.ts" AND file not matches "**/*.test.ts"
test_result == "fail" OR test_count == 0
```

## Avoiding Hook Pitfalls

| Pitfall | Description | Prevention |
|:--------|:------------|:-----------|
| Infinite loop | hook triggers on a file it modifies | add `file not matches` for agent output files |
| Token waste | hook activates on every keystroke or frequent event | add specific conditions to reduce activation frequency |
| Noisy chat | hook produces chat output on common events | direct output to a log file or suppress low-value notifications |
| Unexpected edits | hook agent modifies files beyond its scope | add explicit scope constraints in the hook action |
| Slow workspace | too many hooks activate simultaneously | use `condition` to serialize activation; avoid overlapping triggers |

## Hook Execution Order

When multiple hooks activate for the same event, Kiro executes them in alphabetical filename order. To control execution order, prefix hook files with numbers:

```
.kiro/hooks/
  00-lint-on-save.md
  01-format-on-save.md
  02-test-on-save.md
```

## Disabling Hooks Temporarily

To disable a hook without deleting it, rename it with a `.disabled` extension:

```bash
mv .kiro/hooks/on-save-lint.md .kiro/hooks/on-save-lint.md.disabled
```

Re-enable by removing the `.disabled` extension and reopening the workspace.

## Source References

- [Kiro Docs: Hooks](https://kiro.dev/docs/hooks)
- [Kiro Docs: Hook Events](https://kiro.dev/docs/hooks/events)
- [Kiro Docs: Hook Conditions](https://kiro.dev/docs/hooks/conditions)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now know how to create event-driven hooks that automate repetitive agent actions, configure conditions to avoid noise, and prevent common hook pitfalls.

Next: [Chapter 7: Multi-Model Strategy and Providers](07-multi-model-strategy-and-providers.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 6: Hooks and Automation**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 6: Hooks and Automation` — the `.kiro/hooks/` directory as the event rule store, the Kiro event bus as the trigger dispatcher, and the agent as the action executor.
2. Separate control-plane decisions (which events to hook, condition design) from data-plane execution (agent action invocation, file modification, chat output).
3. Capture input contracts: hook file with event type, condition expression, and action description; output: agent-executed action on trigger.
4. Trace state transitions: hook file written → workspace restart → event bus registers hook → event fires → condition evaluated → agent action invoked → output produced.
5. Identify extension hooks: custom event types via MCP, condition expression extensions, action scope constraints.
6. Map ownership boundaries: developers own feature-specific hooks; team leads own shared hooks in the repository; security team approves hooks that trigger git or publish operations.
7. Specify rollback paths: disable hook by adding `.disabled` extension; revert hook file via git; restart workspace to clear in-flight hook executions.
8. Track observability signals: hook activation frequency, agent action token usage per hook, false-positive activation rate, hook-induced test failures.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Hook scope | narrow file-pattern conditions | broad event hooks with explicit exclusions | simplicity vs coverage |
| Agent action type | read-only analysis and reporting | write operations on source files | safety vs automation level |
| Activation frequency | save-level hooks with debounce | commit-level or task-complete hooks | responsiveness vs cost |
| Output channel | chat panel notifications | log file writes for audit | visibility vs noise |
| Hook governance | individual developer hooks | team-reviewed hooks committed to git | velocity vs consistency |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| infinite loop | hook activates repeatedly on same file | hook modifies the file that triggered it | add exclusion for agent output files in condition |
| token cost spike | unexpectedly high daily token usage | hook activates on high-frequency events without conditions | add specific conditions to reduce activation rate |
| noisy chat | chat panel fills with hook notifications | hook outputs to chat on common events | redirect output to a log file for low-priority hooks |
| unexpected file edit | agent modifies unintended files during hook | underconstrained action description | add explicit "do not modify files other than X" constraint in action |
| hook ordering conflict | two hooks produce conflicting changes to the same file | overlapping hook triggers | use numeric prefix to serialize execution; add mutual exclusion conditions |
| slow workspace | every save triggers multiple concurrent agent invocations | too many broad hooks active simultaneously | audit hook conditions and consolidate overlapping triggers |

### Implementation Runbook

1. Create `.kiro/hooks/` in the project root.
2. Identify the three highest-value repetitive manual workflows in your daily development cycle.
3. Write one hook file per workflow using the event/condition/action format.
4. Save a test file to trigger the first `file:save` hook and verify the agent's action output.
5. Check the agent activity log for the hook invocation and confirm the output is correct.
6. Add numeric prefixes to hooks that share the same event to control execution order.
7. Test the full hook set after a real coding session and identify any noise or false activations.
8. Refine condition expressions to reduce false activations and commit the final hook set.
9. Document each hook's purpose and expected behavior in a `.kiro/hooks/README.md`.

### Quality Gate Checklist

- [ ] all hooks have a condition expression to prevent broad activation
- [ ] no hook modifies a file that could re-trigger the same event (infinite loop prevention)
- [ ] hook action descriptions include explicit scope constraints on file modifications
- [ ] hooks are tested with a real event before committing to version control
- [ ] high-frequency event hooks (file:save) use specific file pattern conditions
- [ ] a hooks README documents each hook's purpose and expected activation rate
- [ ] token usage is monitored after adding new hooks for the first week
- [ ] disabled hooks use the `.disabled` extension naming convention for easy re-enabling

### Source Alignment

- [Kiro Docs: Hooks](https://kiro.dev/docs/hooks)
- [Kiro Docs: Hook Events](https://kiro.dev/docs/hooks/events)
- [Kiro Docs: Hook Conditions](https://kiro.dev/docs/hooks/conditions)
- [Kiro Docs: Hook Action Constraints](https://kiro.dev/docs/hooks/actions)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

### Cross-Tutorial Connection Map

- [Claude Code Tutorial](../claude-code-tutorial/)
- [N8N AI Tutorial](../n8n-ai-tutorial/)
- [Activepieces Tutorial](../activepieces-tutorial/)
- [GitHub MCP Server Tutorial](../github-mcp-server-tutorial/)
- [Chapter 7: Multi-Model Strategy and Providers](07-multi-model-strategy-and-providers.md)

### Advanced Practice Exercises

1. Build a hook that triggers on test failure, analyzes the failing test, and writes a diagnostic summary to a log file.
2. Create a hook that checks documentation freshness when API files are committed and lists stale doc sections.
3. Simulate an infinite loop scenario by creating a hook that modifies the file it watches; then fix it with an exclusion condition.
4. Monitor token usage for one week with three active hooks and calculate the cost per activation for each hook type.
5. Design a hook governance proposal: define which hooks require team review before merging to main and which can be individual developer hooks.

### Review Questions

1. What is the difference between a `file:save` hook and a `git:commit` hook, and when is each more appropriate?
2. How do you prevent an infinite loop when a hook agent modifies a source file?
3. What tradeoff did you make between hook responsiveness (save-level) and token efficiency (commit-level)?
4. How would you recover if a hook introduced a test failure by auto-applying a lint fix that broke logic?
5. What governance process should control hooks that trigger write operations on shared source files?

### Scenario Playbook 1: Hooks - Infinite Loop

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: a file:save hook that applies lint fixes re-triggers itself every time it saves the fixed file
- initial hypothesis: the hook condition does not exclude the files the agent modifies after applying fixes
- immediate action: disable the hook immediately by adding the `.disabled` extension to stop the loop
- engineering control: add `file not matches ".kiro/agent-output/**"` or a similar exclusion to the hook condition
- verification target: save a TypeScript file and confirm the hook activates only once per developer save
- rollback trigger: if the exclusion condition is too broad and blocks legitimate activations, narrow the exclusion pattern
- communication step: document the infinite loop incident and fix in the hooks README
- learning capture: add "check for self-triggering loops" as a required review step in the hook PR checklist

### Scenario Playbook 2: Hooks - Token Cost Spike

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: daily token usage spikes after adding a file:save hook without a file pattern condition
- initial hypothesis: the hook is activating on every file save including node_modules and build artifacts
- immediate action: disable the hook and check the activation log for unexpected trigger files
- engineering control: add a specific file pattern condition: `file matches "src/**/*.ts" AND file not matches "node_modules/**"`
- verification target: token usage returns to baseline levels after the condition is applied
- rollback trigger: if token cost remains high after condition refinement, switch the event to `git:commit` instead of `file:save`
- communication step: share the token cost findings with the team and add a token budget guideline to the hook governance doc
- learning capture: add token cost estimation to the hook design process before activating a new hook in production

### Scenario Playbook 3: Hooks - Noisy Chat Panel

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: the chat panel is filled with low-value hook notifications every time a file is saved
- initial hypothesis: the hook is configured to output its findings to the chat panel for events that occur too frequently
- immediate action: redirect the hook's output from chat to a log file: `.kiro/hook-log.md`
- engineering control: use chat output only for high-priority hooks (test failure analysis, security warnings); use log files for routine hooks
- verification target: chat panel shows only actionable notifications; routine logs are in `.kiro/hook-log.md`
- rollback trigger: if log file grows too large, add a rotation mechanism or summarize logs daily
- communication step: update the hooks README with the output channel conventions for the team
- learning capture: add output channel selection as a required design decision in the hook template

### Scenario Playbook 4: Hooks - Unexpected File Edit

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: a hook agent modifies files beyond the intended scope during a file:save trigger
- initial hypothesis: the hook action description was underspecified and allowed the agent to infer additional scope
- immediate action: revert the unintended file modifications using `git checkout`
- engineering control: add explicit "do not modify files other than the saved file" constraint to the hook action description
- verification target: re-trigger the hook and confirm only the specified file is modified
- rollback trigger: if the constraint causes the hook to produce incomplete output, split into two hooks with different scopes
- communication step: document the out-of-scope modification in the hook's revision history
- learning capture: add scope constraint as a mandatory field in the hook file template

### Scenario Playbook 5: Hooks - Hook Ordering Conflict

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: two hooks triggered by the same file:save event produce conflicting changes to the same file
- initial hypothesis: both hooks modify the same file without coordination, and their execution order is non-deterministic
- immediate action: disable the conflicting hook and manually merge the intended changes
- engineering control: add numeric prefixes to both hooks to enforce serial execution and add a mutual exclusion condition to the second hook
- verification target: save a test file and confirm hook 1 completes before hook 2 activates, with no conflicting changes
- rollback trigger: if serial execution still produces conflicts, merge the two hooks into one combined hook
- communication step: document the merge decision and the new combined hook in the team's hooks change log
- learning capture: add a "check for file overlap with existing hooks" step to the hook PR review checklist

## What Problem Does This Solve?

Repetitive manual workflows are the silent tax on engineering productivity. Every time a developer saves a file and then manually runs lint, checks test failures, and updates documentation, they are doing work that follows a predictable pattern. Kiro hooks eliminate this tax by encoding the "what happens next" logic as event-driven agents that run automatically.

In practical terms, this chapter helps you avoid three common failures:

- letting lint errors accumulate because running the linter is a separate manual step that gets skipped under deadline pressure
- discovering test failures hours after they were introduced because no automated analysis ran at the point of change
- letting documentation drift because doc updates are always "the next task" that never gets done

After working through this chapter, you should be able to treat `.kiro/hooks/` as a team-owned library of automation patterns that encode the team's quality practices as first-class workspace behavior.

## How it Works Under the Hood

Under the hood, `Chapter 6: Hooks and Automation` follows a repeatable control path:

1. **Hook registration**: at workspace open, Kiro scans `.kiro/hooks/` and registers each hook with the event bus.
2. **Event detection**: the Kiro event bus monitors workspace state for registered event types.
3. **Condition evaluation**: when an event fires, Kiro evaluates the hook's condition expression against the event context.
4. **Agent dispatch**: if the condition passes, Kiro dispatches the hook action to an agent with the event context as input.
5. **Action execution**: the agent executes the action, potentially reading files, writing output, or running commands.
6. **Result routing**: the agent's output is routed to the configured channel (chat panel or log file).

When debugging hook issues, verify each stage: hook registered, event fired, condition evaluated, agent dispatched, action completed, output routed.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Docs: Hooks](https://kiro.dev/docs/hooks)
  Why it matters: the primary reference for hook file format, event types, and condition syntax.
- [Kiro Docs: Hook Events](https://kiro.dev/docs/hooks/events)
  Why it matters: documents all available event types and the context data available for condition evaluation.
- [Kiro Docs: Hook Conditions](https://kiro.dev/docs/hooks/conditions)
  Why it matters: defines the condition expression language and supported operators.
- [Kiro Docs: Hook Action Constraints](https://kiro.dev/docs/hooks/actions)
  Why it matters: explains how to scope hook agent actions to prevent unintended side effects.

Suggested trace strategy:
- check the hook events docs for the exact context variables available before writing condition expressions
- test each hook with the minimal possible condition before expanding to broader file pattern matching

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: MCP Integration and External Tools](05-mcp-integration-and-external-tools.md)
- [Next Chapter: Chapter 7: Multi-Model Strategy and Providers](07-multi-model-strategy-and-providers.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 6: Hooks and Automation

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
