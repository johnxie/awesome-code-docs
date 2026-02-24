---
layout: default
title: "Chapter 2: Spec-Driven Development Workflow"
nav_order: 2
parent: Kiro Tutorial
---

# Chapter 2: Spec-Driven Development Workflow

Welcome to **Chapter 2: Spec-Driven Development Workflow**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Kiro's defining innovation is that AI assistance is organized around three structured documents rather than freeform chat. This chapter teaches you how to create, iterate, and execute against specs.

## Learning Goals

- understand the three-file spec structure: requirements.md, design.md, tasks.md
- write requirements using EARS (Easy Approach to Requirements Syntax)
- generate a design document from requirements using Kiro's spec agent
- break design into actionable tasks that Kiro agents can execute
- iterate specs as requirements change without losing design traceability

## Fast Start Checklist

1. open the Kiro Specs panel or navigate to `.kiro/specs/`
2. create a new spec with a feature name (e.g., `user-authentication`)
3. write at least three requirements in EARS format in `requirements.md`
4. ask Kiro to generate `design.md` from the requirements
5. ask Kiro to generate `tasks.md` from the design
6. execute the first task

## The Three-File Spec Structure

```
.kiro/
  specs/
    user-authentication/
      requirements.md   ← what the feature must do (EARS syntax)
      design.md         ← how to build it (architecture, data models, APIs)
      tasks.md          ← numbered implementation steps for the agent
```

Each spec lives in its own named folder under `.kiro/specs/`. Committing these files to version control gives your team a living record of AI-assisted design decisions.

## EARS Syntax for Requirements

EARS (Easy Approach to Requirements Syntax) is a structured natural-language format for writing unambiguous requirements. Kiro expects requirements in this format to generate high-quality design and task documents.

| EARS Pattern | Template | Example |
|:-------------|:---------|:--------|
| Ubiquitous | The `<system>` shall `<action>`. | The system shall hash passwords using bcrypt. |
| Event-driven | When `<trigger>`, the `<system>` shall `<action>`. | When a user submits a login form, the system shall validate credentials against the database. |
| Unwanted behavior | If `<condition>`, then the `<system>` shall `<action>`. | If credentials are invalid, then the system shall return a 401 response with an error message. |
| State-driven | While `<state>`, the `<system>` shall `<action>`. | While a session is active, the system shall refresh the JWT token every 15 minutes. |
| Optional feature | Where `<feature>` is supported, the `<system>` shall `<action>`. | Where MFA is enabled, the system shall require a TOTP code at login. |

## Writing requirements.md

```markdown
# Requirements: User Authentication

## Functional Requirements

- The system shall store user credentials with bcrypt-hashed passwords at cost factor 12.
- When a user submits valid credentials, the system shall issue a signed JWT with a 1-hour expiry.
- If credentials are invalid, then the system shall return HTTP 401 with a generic error message.
- While a session is active, the system shall refresh the JWT automatically 5 minutes before expiry.
- When a user requests logout, the system shall invalidate the session token immediately.

## Non-Functional Requirements

- The system shall complete credential validation in under 200ms at p95.
- If the authentication service is unavailable, then the system shall return HTTP 503 within 5 seconds.
```

## Generating design.md

Once requirements are written, ask Kiro to generate the design:

```
# In the Chat panel:
> Generate a design document for the user-authentication spec based on requirements.md

# Kiro reads requirements.md and produces design.md covering:
# - component architecture (auth service, token store, session manager)
# - data models (User, Session, RefreshToken)
# - API contracts (POST /auth/login, POST /auth/logout, POST /auth/refresh)
# - error handling strategy
# - security considerations
```

A sample `design.md` excerpt:

```markdown
# Design: User Authentication

## Architecture

The authentication feature uses a three-layer model:
- API layer: Express routes for /auth/login, /auth/logout, /auth/refresh
- Service layer: AuthService with validateCredentials(), issueToken(), revokeToken()
- Data layer: PostgreSQL users table, Redis session store for token revocation

## Data Models

### User
| Field | Type | Constraints |
|:------|:-----|:-----------|
| id | UUID | primary key |
| email | VARCHAR(255) | unique, not null |
| password_hash | VARCHAR(60) | bcrypt, not null |
| created_at | TIMESTAMP | not null |

## API Contracts

POST /auth/login
  Body: { email: string, password: string }
  Success: 200 { token: string, expires_at: ISO8601 }
  Failure: 401 { error: "invalid_credentials" }
```

## Generating tasks.md

After the design is approved, ask Kiro to generate the task list:

```
> Generate a tasks.md implementation plan from design.md

# Kiro produces a numbered task list such as:
```

```markdown
# Tasks: User Authentication

- [ ] 1. Create PostgreSQL migration for users table with id, email, password_hash, created_at
- [ ] 2. Implement AuthService.validateCredentials() with bcrypt comparison
- [ ] 3. Implement AuthService.issueToken() using jsonwebtoken with 1h expiry
- [ ] 4. Implement AuthService.revokeToken() using Redis SET with TTL
- [ ] 5. Create POST /auth/login route with input validation and AuthService calls
- [ ] 6. Create POST /auth/logout route that calls revokeToken()
- [ ] 7. Create POST /auth/refresh route with automatic token renewal
- [ ] 8. Add middleware to verify JWT on protected routes
- [ ] 9. Write unit tests for AuthService methods
- [ ] 10. Write integration tests for all /auth routes
```

## Executing Tasks

You can execute tasks one by one or delegate them to the autonomous agent:

```
# Execute a single task:
> Complete task 1: create the PostgreSQL migration for the users table

# Delegate all tasks to the agent:
> Execute all tasks in tasks.md for the user-authentication spec
```

## Iterating Specs

When requirements change, update `requirements.md` first, then regenerate downstream documents:

```
> requirements.md has been updated to add MFA support. Regenerate design.md to include TOTP handling.

# After confirming design.md:
> Regenerate tasks.md to include the new MFA tasks from design.md
```

## Source References

- [Kiro Docs: Specs](https://kiro.dev/docs/specs)
- [Kiro Docs: EARS Syntax](https://kiro.dev/docs/specs/ears)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now understand how to create, generate, and execute three-file specs in Kiro using EARS requirements syntax.

Next: [Chapter 3: Agent Steering and Rules Configuration](03-agent-steering-and-rules-configuration.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 2: Spec-Driven Development Workflow**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 2: Spec-Driven Development Workflow` — the `.kiro/specs/` directory as the source of truth, the spec agent as transformer, and the chat panel as the control interface.
2. Separate control-plane decisions (which requirements to include, design approval gates) from data-plane execution (file writes, task execution).
3. Capture input contracts: EARS-formatted `requirements.md`; output contracts: approved `design.md` and executable `tasks.md`.
4. Trace state transitions: empty spec folder → requirements written → design generated → design approved → tasks generated → tasks executing → tasks complete.
5. Identify extension hooks: custom EARS templates, design document templates, task numbering conventions.
6. Map ownership boundaries: product/engineer owns `requirements.md`; architect reviews `design.md`; agent executes `tasks.md`.
7. Specify rollback paths: revert `design.md` to a previous git commit; regenerate `tasks.md` from the prior design.
8. Track observability signals: spec generation latency, task completion rate, requirement traceability coverage.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Requirements granularity | 5-10 high-level EARS statements | 20+ detailed acceptance criteria | speed vs precision |
| Design approval gate | developer self-approves | architect review before task generation | velocity vs quality |
| Task delegation | manual task-by-task execution | full autonomous delegation | control vs efficiency |
| Spec versioning | file in .kiro/ only | committed to git with PR review | simplicity vs auditability |
| Iteration strategy | regenerate full design on change | diff-patch specific sections | speed vs traceability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| ambiguous requirements | design doc misses intent | vague EARS statements | add acceptance criteria and examples to each requirement |
| design drift | tasks diverge from design | design.md edited without regenerating tasks | treat design.md as source of truth; always regenerate tasks after edits |
| task scope creep | tasks grow beyond spec | underconstrained task generation | add a "scope boundary" section to design.md |
| stale spec | code diverges from requirements | no enforcement of spec-first updates | add a CI check that alerts when code changes lack a corresponding spec update |
| overgenerated tasks | too many micro-tasks slow progress | fine-grained design decomposition | set a max-tasks constraint in the spec generation prompt |
| spec format violations | agent rejects or misreads spec | non-EARS requirements | validate requirements.md against EARS patterns before generation |

### Implementation Runbook

1. Create the spec directory: `.kiro/specs/<feature-name>/`.
2. Write `requirements.md` using EARS syntax with at least three functional and one non-functional requirement.
3. Ask Kiro to generate `design.md` from `requirements.md` and review the output for completeness.
4. Identify any gaps in the design and add clarifying context to `requirements.md`, then regenerate.
5. Approve `design.md` by committing it to version control with a design-review tag.
6. Ask Kiro to generate `tasks.md` from `design.md` and verify task ordering and dependencies.
7. Execute the first two tasks manually to validate the spec-to-code translation quality.
8. Promote remaining tasks to autonomous agent execution after manual validation.
9. Mark completed tasks in `tasks.md` and commit the updated spec after each task group completes.

### Quality Gate Checklist

- [ ] all requirements are written in valid EARS syntax with no ambiguous "should" language
- [ ] `design.md` covers component architecture, data models, API contracts, and error handling
- [ ] `tasks.md` is numbered, ordered by dependency, and each task references the design section it implements
- [ ] spec files are committed to version control before task execution begins
- [ ] at least two tasks are manually validated before autonomous delegation
- [ ] a rollback path (git revert of spec files) is documented and tested
- [ ] spec generation latency is within acceptable bounds for the team's workflow
- [ ] requirement traceability is confirmed: every task maps to at least one requirement

### Source Alignment

- [Kiro Docs: Specs](https://kiro.dev/docs/specs)
- [Kiro Docs: EARS Syntax](https://kiro.dev/docs/specs/ears)
- [Kiro Docs: Task Execution](https://kiro.dev/docs/specs/tasks)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

### Cross-Tutorial Connection Map

- [Claude Code Tutorial](../claude-code-tutorial/)
- [Cline Tutorial](../cline-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [Plandex Tutorial](../plandex-tutorial/)
- [Chapter 3: Agent Steering and Rules Configuration](03-agent-steering-and-rules-configuration.md)

### Advanced Practice Exercises

1. Write a complete `requirements.md` for a payment processing feature using all five EARS patterns.
2. Generate `design.md` and identify one gap; update requirements and regenerate to confirm the gap is filled.
3. Simulate a requirement change mid-execution and practice updating only the affected tasks in `tasks.md`.
4. Add a CI check that lints `requirements.md` for non-EARS language like "should" or "might".
5. Compare the task output from two different levels of design granularity and measure execution accuracy.

### Review Questions

1. What is the purpose of EARS syntax and why does Kiro require it for high-quality spec generation?
2. Which approval gate prevents design drift from propagating into task execution?
3. What tradeoff did you make between task granularity and autonomous delegation speed?
4. How would you recover if `design.md` was edited manually and `tasks.md` is now inconsistent?
5. What must be in version control before autonomous task execution begins?

### Scenario Playbook 1: Spec Generation - Ambiguous Requirements

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: design.md misses key business logic because requirements.md used vague language
- initial hypothesis: identify which EARS statements lack acceptance criteria or measurable conditions
- immediate action: add concrete examples and edge cases to the failing requirements before regenerating
- engineering control: require peer review of requirements.md before submitting to the spec agent
- verification target: every requirement in the regenerated design.md maps to a specific, testable implementation
- rollback trigger: if two regeneration attempts still miss key logic, escalate to a design workshop with the team
- communication step: document the ambiguous requirements and their clarified versions in the spec PR description
- learning capture: add the clarified examples to the team's EARS writing guide for future features

### Scenario Playbook 2: Spec Generation - Design Drift

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tasks.md references components or APIs that no longer match design.md after manual edits
- initial hypothesis: diff design.md against its last committed version to identify manual changes
- immediate action: revert design.md to the last approved commit and regenerate tasks.md
- engineering control: treat design.md as an append-only document; add new sections rather than editing existing ones
- verification target: every task in tasks.md references a section that exists in the current design.md
- rollback trigger: if task regeneration continues to produce drift, split the spec into two separate feature specs
- communication step: notify the team that design.md has a new version and tasks.md has been regenerated
- learning capture: add a git hook that warns when design.md is modified without a corresponding tasks.md regeneration

### Scenario Playbook 3: Spec Execution - Task Scope Creep

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: autonomous agent adds files or changes outside the defined task scope during execution
- initial hypothesis: review the task description for missing scope boundaries or implicit dependencies
- immediate action: halt agent execution, review changes, and revert any out-of-scope modifications
- engineering control: add an explicit "out of scope" section to tasks.md listing what the agent must not change
- verification target: agent changes are confined to the files and directories listed in the task description
- rollback trigger: if out-of-scope changes recur on the next task, switch to manual task-by-task execution
- communication step: document the out-of-scope incident in the spec's revision history
- learning capture: update the task generation prompt template to always include a scope boundary constraint

### Scenario Playbook 4: Spec Iteration - Mid-Sprint Requirement Change

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: a product decision changes one requirement after task execution has already begun
- initial hypothesis: identify which completed tasks are affected by the changed requirement
- immediate action: mark affected completed tasks as "needs-revision" in tasks.md and halt further execution
- engineering control: update requirements.md first, then regenerate only the affected design.md sections and tasks
- verification target: updated tasks are re-executed and produce output consistent with the new requirement
- rollback trigger: if the change invalidates more than 50% of completed tasks, create a new spec branch
- communication step: update the PR description with the requirement change and its impact on the task list
- learning capture: add a "change impact" section to the spec template for documenting mid-sprint pivots

### Scenario Playbook 5: Spec Quality - Stale Spec After Code Refactor

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: code has been refactored but the spec files still reference the old architecture
- initial hypothesis: compare the current codebase structure against design.md component references
- immediate action: flag the spec as "stale" and schedule a spec refresh session before the next feature build
- engineering control: add a quarterly spec audit to the team's engineering calendar
- verification target: refreshed design.md accurately describes the current architecture and data models
- rollback trigger: if the spec refresh reveals architectural inconsistencies, escalate to an architecture review
- communication step: announce the spec refresh in the team channel and request review from senior engineers
- learning capture: add a "last verified" timestamp field to each spec and enforce it in the PR template

## What Problem Does This Solve?

Most agentic coding tools suffer from the "chat amnesia" problem: each conversation starts fresh, there is no persistent record of design decisions, and AI-generated code accumulates without traceability back to requirements. Kiro's spec-driven workflow solves this by making the design artifact — not the conversation — the primary interface for AI assistance.

In practical terms, this chapter helps you avoid three common failures:

- generating code that satisfies the immediate prompt but misses the broader system design
- losing context across sessions when working on a multi-day feature
- having no audit trail of why specific implementation choices were made

After working through this chapter, you should be able to reason about Kiro specs as a contract layer between product intent, system design, and agent execution — with explicit traceability from requirement to code.

## How it Works Under the Hood

Under the hood, `Chapter 2: Spec-Driven Development Workflow` follows a repeatable control path:

1. **Spec directory initialization**: Kiro creates `.kiro/specs/<feature>/` and registers the spec in the workspace index.
2. **Requirements parsing**: the spec agent reads `requirements.md` and classifies each statement by EARS pattern type.
3. **Design generation**: the agent maps requirements to components, data models, and APIs and writes `design.md`.
4. **Design approval gate**: the developer reviews and commits `design.md`; Kiro treats the committed version as canonical.
5. **Task decomposition**: the agent reads `design.md` and generates ordered, dependency-aware tasks in `tasks.md`.
6. **Task execution loop**: each task is dispatched to the appropriate execution agent with the design as grounding context.

When debugging spec quality issues, walk this sequence in order and check the output at each stage before moving forward.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Docs: Specs](https://kiro.dev/docs/specs)
  Why it matters: the authoritative reference for the three-file spec format and generation workflow.
- [Kiro Docs: EARS Syntax](https://kiro.dev/docs/specs/ears)
  Why it matters: defines the exact EARS patterns Kiro uses to parse and classify requirements.
- [Kiro Docs: Task Execution](https://kiro.dev/docs/specs/tasks)
  Why it matters: documents how tasks.md items are dispatched to agents and how completion is tracked.
- [Kiro Repository](https://github.com/kirodotdev/Kiro)
  Why it matters: source of truth for spec agent implementation and community-contributed spec templates.

Suggested trace strategy:
- search the Kiro docs for each EARS pattern keyword before writing your first requirements.md
- compare generated design.md sections against the design template in the docs to confirm coverage

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started](01-getting-started.md)
- [Next Chapter: Chapter 3: Agent Steering and Rules Configuration](03-agent-steering-and-rules-configuration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
