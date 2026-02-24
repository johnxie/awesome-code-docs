---
layout: default
title: "Chapter 4: Autonomous Agent Mode"
nav_order: 4
parent: Kiro Tutorial
---

# Chapter 4: Autonomous Agent Mode

Welcome to **Chapter 4: Autonomous Agent Mode**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Kiro's autonomous agent mode delegates multi-step execution to an AI agent that can read files, write code, run terminal commands, and iterate — all without manual approval of each step. This chapter teaches you how to delegate safely and monitor effectively.

## Learning Goals

- understand the difference between interactive chat and autonomous agent execution
- configure autonomy levels and approval gates for different task types
- delegate complete tasks from tasks.md to the autonomous agent
- monitor agent progress and intervene when needed
- define safe boundaries for autonomous execution in production-adjacent environments

## Fast Start Checklist

1. open a tasks.md with at least one uncompleted task
2. select the task and choose "Execute with Agent" in the Kiro interface
3. observe the agent's step-by-step execution in the Agent Activity panel
4. verify the output files and test results after completion
5. mark the task as complete in tasks.md

## Autonomous vs. Interactive Mode

| Mode | Agent Behavior | Approval Required | Best For |
|:-----|:---------------|:-----------------|:---------|
| Interactive Chat | responds to each message, waits for next | every step | exploratory work, design discussion |
| Supervised Agent | executes steps, pauses at risk boundaries | pre-configured risk points | complex tasks with clear specs |
| Autonomous Agent | executes full task end-to-end | none during execution | well-specified tasks from tasks.md |

## Autonomy Levels

Kiro supports three autonomy levels that control how much the agent does before stopping for human input:

| Level | Description | Stops When |
|:------|:------------|:-----------|
| Cautious | executes one sub-step at a time | after every file write or command |
| Balanced | executes logical task groups | before destructive commands or large rewrites |
| Full | executes the complete task | only on error or completion |

Configure the autonomy level in `.kiro/settings.json`:

```json
{
  "agent": {
    "autonomyLevel": "balanced",
    "allowedCommands": ["npm test", "npm run build", "npx prisma migrate dev"],
    "forbiddenCommands": ["rm -rf", "git push --force", "npm publish"],
    "maxFileEditsPerTask": 20,
    "requireApprovalForNewFiles": false
  }
}
```

## Delegating a Task

```
# In the Chat panel with tasks.md open:
> Execute task 3: implement AuthService.issueToken() using jsonwebtoken with 1h expiry

# The agent will:
# 1. Read design.md for the AuthService interface contract
# 2. Read the current src/auth/auth.service.ts file
# 3. Write the issueToken() implementation
# 4. Run the relevant unit tests
# 5. Report completion or errors
```

## Agent Activity Panel

During autonomous execution, the Agent Activity panel shows the agent's step-by-step reasoning:

```
[Agent] Reading design.md for AuthService interface...
[Agent] Reading src/auth/auth.service.ts...
[Agent] Writing issueToken() implementation...
  + Added import { sign } from 'jsonwebtoken'
  + Added issueToken(userId: string): string method
[Agent] Running: npm test -- --testPathPattern=auth.service
  PASS src/auth/auth.service.test.ts (3 tests passed)
[Agent] Task 3 complete. 1 file modified, 3 tests passing.
```

## Interrupting Agent Execution

You can interrupt the agent at any point:

```
# Press Escape or click "Stop Agent" in the activity panel

# After stopping:
> What did you complete before I interrupted you?
# Agent summarizes completed sub-steps

# Review and decide whether to:
# - Resume from the last checkpoint
# - Discard changes and restart
# - Complete the remaining steps manually
```

## Safe Boundaries for Autonomous Execution

Define boundaries before delegating autonomous tasks, especially in shared or production-adjacent environments:

```markdown
# Safe for autonomous execution:
- Writing new source files in src/
- Modifying test files
- Running unit and integration tests
- Installing dev dependencies
- Running database migrations in test environments

# Requires human approval:
- Modifying .env files or secrets
- Pushing to remote branches
- Running database migrations in staging or production
- Publishing packages
- Deleting files (except test artifacts)
```

## Multi-Step Task Delegation

For complex features, delegate multiple sequential tasks:

```
> Execute tasks 1 through 5 in tasks.md for the user-authentication spec.
  Stop after each task group and show me what was completed before proceeding.

# Agent executes:
# Task 1: database migration → reports completion
# Task 2: AuthService.validateCredentials() → reports completion
# Task 3: AuthService.issueToken() → reports completion
# [pauses for review]
# Task 4: AuthService.revokeToken() → reports completion
# Task 5: POST /auth/login route → reports completion
# [pauses for review]
```

## Error Recovery in Autonomous Mode

When the agent encounters an error, it attempts self-correction:

```
[Agent] Running: npm test -- --testPathPattern=auth.service
  FAIL src/auth/auth.service.test.ts
  ● AuthService › issueToken › should return a valid JWT
    Expected: string matching /^ey/
    Received: undefined

[Agent] Analyzing test failure...
[Agent] Issue found: JWT_SECRET environment variable not set in test environment
[Agent] Fixing: adding JWT_SECRET to jest.config.ts testEnvironment setup...
[Agent] Running tests again...
  PASS src/auth/auth.service.test.ts (3 tests passed)
[Agent] Task 3 complete after one self-correction.
```

## Source References

- [Kiro Docs: Autonomous Agent](https://kiro.dev/docs/agent)
- [Kiro Docs: Autonomy Levels](https://kiro.dev/docs/agent/autonomy)
- [Kiro Docs: Agent Activity](https://kiro.dev/docs/agent/activity)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now know how to delegate tasks to Kiro's autonomous agent, configure autonomy levels, monitor execution, and define safe operational boundaries.

Next: [Chapter 5: MCP Integration and External Tools](05-mcp-integration-and-external-tools.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 4: Autonomous Agent Mode**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 4: Autonomous Agent Mode` — the agent executor, the tool dispatch layer, and the approval gate controller.
2. Separate control-plane decisions (autonomy level, allowed commands, approval gates) from data-plane execution (file writes, test runs, self-correction loops).
3. Capture input contracts: a task description from tasks.md with spec context; output: completed code changes and passing tests.
4. Trace state transitions: task selected → agent plan generated → sub-steps executing → error or completion → human review.
5. Identify extension hooks: `allowedCommands`, `forbiddenCommands`, `maxFileEditsPerTask`, and custom approval triggers.
6. Map ownership boundaries: developer owns task delegation decisions; team leads own autonomy level configuration; security team approves `allowedCommands` list.
7. Specify rollback paths: `git checkout` to revert agent changes; restore from task checkpoint if execution was interrupted.
8. Track observability signals: agent activity log, test pass/fail rates, self-correction frequency, task completion time.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Autonomy level | cautious (one step at a time) | full autonomy for well-specified tasks | control vs efficiency |
| Command allowlist | no shell commands | narrow allowlist of known-safe commands | safety vs capability |
| Task scope | single task delegation | multi-task sequential delegation | simplicity vs throughput |
| Error recovery | human intervention on first error | agent self-correction with logging | oversight vs speed |
| Rollback strategy | manual git checkout | automated checkpoint and revert | effort vs recovery speed |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| agent scope creep | unexpected file edits outside task scope | underconstrained task description | add explicit file scope to task description |
| runaway command execution | agent runs commands not in allowlist | missing `forbiddenCommands` config | maintain an explicit `forbiddenCommands` list in settings |
| self-correction loop | agent retries same failing pattern | root cause not identified before retry | set max self-correction attempts; escalate to human on limit |
| context window overflow | agent loses task context mid-execution | very long task with many sub-steps | split long tasks into smaller independent tasks |
| environment mismatch | tests pass locally but agent tests fail | agent uses different Node or env vars | standardize the test environment in jest.config.ts |
| partial completion without reporting | agent stops mid-task without clear status | error swallowed by recovery logic | require agent to log completion status for every sub-step |

### Implementation Runbook

1. Define the autonomy level for the current task profile in `.kiro/settings.json`.
2. Review and set the `allowedCommands` list to only include commands safe for automated execution.
3. Confirm the task in tasks.md has a clear, bounded scope with references to specific files or modules.
4. Delegate the task via the Chat panel or the Specs task list interface.
5. Monitor the Agent Activity panel during execution and verify each sub-step output.
6. If the agent self-corrects, review the correction log to confirm the fix is sound.
7. After task completion, run the full test suite manually to verify no regressions were introduced.
8. Review the git diff to confirm changes are scoped to the expected files.
9. Mark the task as complete in tasks.md and commit the updated spec.

### Quality Gate Checklist

- [ ] autonomy level is configured appropriately for the task type before delegation
- [ ] `allowedCommands` and `forbiddenCommands` are explicitly set in `.kiro/settings.json`
- [ ] task description includes explicit file scope to prevent agent scope creep
- [ ] agent activity log is reviewed after each task for unexpected behavior
- [ ] self-correction events are counted and investigated for root cause
- [ ] full test suite passes after autonomous task completion
- [ ] git diff is reviewed to confirm no out-of-scope changes
- [ ] task completion is marked in tasks.md and committed to version control

### Source Alignment

- [Kiro Docs: Autonomous Agent](https://kiro.dev/docs/agent)
- [Kiro Docs: Autonomy Levels](https://kiro.dev/docs/agent/autonomy)
- [Kiro Docs: Agent Activity](https://kiro.dev/docs/agent/activity)
- [Kiro Docs: Settings](https://kiro.dev/docs/settings)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

### Cross-Tutorial Connection Map

- [OpenHands Tutorial](../openhands-tutorial/)
- [SWE-Agent Tutorial](../swe-agent-tutorial/)
- [AutoGen Tutorial](../autogen-tutorial/)
- [CrewAI Tutorial](../crewai-tutorial/)
- [Chapter 5: MCP Integration and External Tools](05-mcp-integration-and-external-tools.md)

### Advanced Practice Exercises

1. Configure three different autonomy levels in `.kiro/settings.json` and test each with the same task to compare output quality and speed.
2. Deliberately give the agent an ambiguous task and observe where it gets confused; then rewrite the task with explicit scope and compare outcomes.
3. Simulate an agent self-correction scenario by introducing a test environment variable that is missing; confirm the agent detects and fixes the issue.
4. Set up a post-task git diff review workflow and practice identifying out-of-scope changes from three different autonomous executions.
5. Build a multi-task delegation sequence for a five-task feature and practice the pause-and-review pattern between task groups.

### Review Questions

1. What determines whether the "balanced" or "full" autonomy level is appropriate for a given task?
2. How do `allowedCommands` and `forbiddenCommands` interact, and what happens if a command appears in neither list?
3. What tradeoff did you make between autonomous efficiency and oversight granularity?
4. How would you recover if the agent completed tasks 1-3 but made an error in task 2 that was only discovered after task 3 completed?
5. What conditions must be true before delegating a task to full autonomous mode without per-step review?

### Scenario Playbook 1: Autonomous Agent - Scope Creep

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: autonomous agent modifies files outside the task's defined scope
- initial hypothesis: task description lacked explicit file boundaries causing the agent to infer additional scope
- immediate action: interrupt the agent and run `git checkout` to revert out-of-scope changes
- engineering control: add explicit file path constraints to the task description before re-delegating
- verification target: re-run the task and confirm only expected files appear in the git diff
- rollback trigger: if scope creep recurs, switch to cautious autonomy level for this task type
- communication step: document the scope creep incident in the task's completion notes
- learning capture: update the task generation prompt to always include an explicit "files to modify" constraint

### Scenario Playbook 2: Autonomous Agent - Runaway Command Execution

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent attempts to run a command not on the allowedCommands list
- initial hypothesis: the command was implied by the task but not explicitly listed in the allowed list
- immediate action: the agent should be blocked by the forbiddenCommands check; if not, stop execution immediately
- engineering control: audit the allowedCommands list and add the missing command if it is safe; update forbiddenCommands otherwise
- verification target: agent is blocked from the command on the next execution attempt
- rollback trigger: if the agent bypassed the command check, report as a security incident to the Kiro team
- communication step: update the team's Kiro security policy with the new command classification
- learning capture: add the new command to the appropriate list and commit the settings.json update with a PR review

### Scenario Playbook 3: Autonomous Agent - Infinite Self-Correction Loop

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent retries the same failing test pattern more than three times without progress
- initial hypothesis: agent is not identifying the true root cause and is applying surface-level fixes
- immediate action: interrupt the agent and manually diagnose the test failure
- engineering control: set a maximum self-correction attempt count in the agent settings
- verification target: after manual fix, re-delegate the task and confirm completion on first attempt
- rollback trigger: if the failure pattern is systemic, escalate to a debugging session with the full team
- communication step: document the root cause and manual fix in the task completion notes
- learning capture: add the root cause pattern to the project steering file's troubleshooting section

### Scenario Playbook 4: Autonomous Agent - Context Window Overflow

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent loses coherence mid-task on a large feature with many sub-steps
- initial hypothesis: the task description plus design context exceeds the model's effective context window
- immediate action: interrupt the agent and split the task into two independent smaller tasks in tasks.md
- engineering control: set a `maxFileEditsPerTask` limit in settings.json to force task splitting at design time
- verification target: each smaller task completes independently without context loss
- rollback trigger: if splitting creates unresolvable dependencies, escalate to manual implementation of the transition step
- communication step: update tasks.md to document the split and the dependency between the two new tasks
- learning capture: add a task complexity guideline to the team's spec writing standards

### Scenario Playbook 5: Autonomous Agent - Partial Completion Without Status

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent stops executing mid-task without reporting completion or error status
- initial hypothesis: an unhandled exception in the agent execution loop caused a silent exit
- immediate action: check the Kiro logs for the last recorded sub-step and manually continue from that point
- engineering control: require the agent to write a checkpoint file after each sub-step for crash recovery
- verification target: after the fix, re-running the task resumes from the last checkpoint without duplicating work
- rollback trigger: if checkpoint recovery produces duplicate code, revert to the pre-task git state and restart
- communication step: report the silent exit as a bug to the Kiro issue tracker with the relevant log snippet
- learning capture: add a post-task verification step that confirms the agent reported a terminal status before marking the task complete

## What Problem Does This Solve?

The fundamental bottleneck in AI-assisted development is not model quality — it is the human-in-the-loop approval rate. When every file edit requires a manual "yes", developers spend more time approving than designing. Kiro's autonomous agent mode removes this bottleneck for well-specified tasks by delegating end-to-end execution while preserving human control at the configuration level.

In practical terms, this chapter helps you avoid three common failures:

- treating the AI as a typing accelerator rather than a true task delegate
- delegating tasks without clear boundaries and getting unexpected side effects
- losing confidence in autonomous mode because errors are not surfaced or recoverable

After working through this chapter, you should be able to reason about autonomous delegation as a spectrum with explicit configuration knobs — not a binary "trust everything" or "approve everything" choice.

## How it Works Under the Hood

Under the hood, `Chapter 4: Autonomous Agent Mode` follows a repeatable control path:

1. **Task ingestion**: the agent reads the task description and fetches the spec context from `design.md`.
2. **Plan generation**: the agent decomposes the task into ordered sub-steps with explicit tool calls.
3. **Tool dispatch**: each sub-step invokes a Kiro tool: file read, file write, shell command, or test runner.
4. **Output validation**: the agent checks each tool output against its expected result before proceeding.
5. **Self-correction loop**: on unexpected output, the agent applies a fix hypothesis and retries up to the configured limit.
6. **Completion reporting**: the agent writes a structured completion report to the Agent Activity log.

When debugging autonomous failures, check each stage in sequence and look for the first sub-step where the output diverged from expectation.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Docs: Autonomous Agent](https://kiro.dev/docs/agent)
  Why it matters: the primary reference for agent capabilities, tool dispatch, and execution lifecycle.
- [Kiro Docs: Autonomy Levels](https://kiro.dev/docs/agent/autonomy)
  Why it matters: documents the exact behavior of each autonomy level and its approval gate logic.
- [Kiro Docs: Agent Activity](https://kiro.dev/docs/agent/activity)
  Why it matters: explains the activity panel format and how to read the sub-step execution log.
- [Kiro Docs: Settings](https://kiro.dev/docs/settings)
  Why it matters: reference for all configurable agent parameters including `allowedCommands` and `maxFileEditsPerTask`.

Suggested trace strategy:
- check the autonomy levels docs before each new task type to select the right configuration
- review the agent activity log after every autonomous execution to build intuition for normal vs. anomalous behavior

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Agent Steering and Rules Configuration](03-agent-steering-and-rules-configuration.md)
- [Next Chapter: Chapter 5: MCP Integration and External Tools](05-mcp-integration-and-external-tools.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
