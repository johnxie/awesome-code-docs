---
layout: default
title: "Chapter 3: Agent Steering and Rules Configuration"
nav_order: 3
parent: Kiro Tutorial
---

# Chapter 3: Agent Steering and Rules Configuration

Welcome to **Chapter 3: Agent Steering and Rules Configuration**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Kiro's steering system lets you encode persistent, project-scoped rules that guide AI behavior without repeating them in every prompt. This chapter teaches you how to build and manage the `.kiro/steering/` directory.

## Learning Goals

- understand the purpose and structure of the `.kiro/steering/` directory
- create steering files that encode technology choices, coding conventions, and project context
- use inclusion and exclusion patterns to scope steering rules to specific file types or directories
- combine multiple steering files for layered, composable rule sets
- troubleshoot steering conflicts and priority ordering

## Fast Start Checklist

1. create `.kiro/steering/` in your project root
2. create `project.md` with your stack, conventions, and key decisions
3. create `coding-style.md` with language-specific style rules
4. verify the steering files are loaded by asking Kiro a question that requires the rules
5. commit `.kiro/steering/` to version control for team sharing

## The Steering Directory Structure

```
.kiro/
  steering/
    project.md          ← always-active project context and technology decisions
    coding-style.md     ← language and framework style conventions
    testing.md          ← testing strategy and framework preferences
    security.md         ← security policies and forbidden patterns
    api-contracts.md    ← API design rules and backward compatibility requirements
```

Steering files are plain markdown. Kiro reads all files in `.kiro/steering/` and injects their content as persistent context for every agent interaction in the workspace.

## Steering File Format

```markdown
# Project Context

## Technology Stack
- Runtime: Node.js 20 with TypeScript strict mode
- Framework: Express 4 with class-validator for input validation
- Database: PostgreSQL 15 with Prisma ORM
- Testing: Jest with ts-jest, supertest for integration tests
- Deployment: AWS Lambda with the Serverless Framework

## Key Decisions
- All new API routes must follow RESTful conventions with plural resource names.
- Use async/await throughout; no raw Promise chains.
- All database queries must go through Prisma; no raw SQL.
- Error responses must use the standard { error: string, code: string } shape.

## Forbidden Patterns
- Never use `any` type in TypeScript.
- Never commit secrets or API keys; use AWS Secrets Manager references.
- Never use synchronous file I/O in request handlers.
```

## Scoped Steering with Inclusion Patterns

You can scope a steering file to apply only when working on specific directories or file types:

```markdown
---
applies_to:
  - "src/api/**"
  - "*.route.ts"
---

# API Route Conventions

- All routes must use express-validator for request body validation.
- Route handlers must be thin: delegate business logic to service classes.
- Return 201 for resource creation, 200 for reads and updates, 204 for deletions.
- Never return raw database error messages to clients.
```

## Example: Security Steering File

```markdown
# Security Policy

## Authentication
- All endpoints except /auth/login and /health must require a valid JWT.
- JWTs must be verified using the RS256 algorithm.
- Never log full JWT tokens; log only the token's jti claim.

## Input Handling
- All user inputs must be validated and sanitized before use.
- Use parameterized queries for all database operations.
- Reject requests with payloads over 1MB with HTTP 413.

## Dependency Policy
- Audit new npm packages with `npm audit` before adding to package.json.
- Pin all production dependency versions; use ranges only for devDependencies.
```

## Example: Testing Steering File

```markdown
# Testing Conventions

## Unit Tests
- Use describe/it blocks with descriptive names that read like sentences.
- Mock all external dependencies (database, HTTP calls) in unit tests.
- Target 80% branch coverage for all service classes.

## Integration Tests
- Use a dedicated test database seeded from fixtures.
- Test the full HTTP stack with supertest; do not mock Express.
- Reset the database state between test suites using beforeEach hooks.

## Test Naming
- Unit test files: `<filename>.test.ts` next to the source file.
- Integration test files: `tests/integration/<feature>.integration.test.ts`.
```

## Combining Steering Files

Kiro merges all active steering files into a single context block. The order of injection follows alphabetical filename order. To control priority, prefix files with numbers:

```
.kiro/steering/
  00-project.md       ← highest priority, always active
  01-coding-style.md
  02-testing.md
  03-security.md
  10-api-contracts.md
```

## Verifying Steering is Active

```
# In the Chat panel:
> What testing framework should I use for this project?

# Expected response (with testing.md loaded):
# Based on the project steering, you should use Jest with ts-jest for unit tests
# and supertest for integration tests.

# If Kiro responds with a generic answer, check:
# 1. .kiro/steering/ exists and contains markdown files
# 2. The files have valid markdown content (no syntax errors)
# 3. The workspace was reopened after adding steering files
```

## Steering vs. Chat Prompts

| Aspect | Steering Files | Chat Prompts |
|:-------|:---------------|:-------------|
| Persistence | permanent, loaded every session | session-only |
| Scope | project-wide or file-scoped | per-conversation |
| Version controlled | yes, committed to git | no |
| Shared with team | yes | no |
| Use for | technology decisions, conventions, policies | specific tasks and one-off instructions |

## Source References

- [Kiro Docs: Steering](https://kiro.dev/docs/steering)
- [Kiro Docs: Steering Files](https://kiro.dev/docs/steering/files)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now know how to create, scope, and combine steering files that encode persistent project rules for Kiro agents.

Next: [Chapter 4: Autonomous Agent Mode](04-autonomous-agent-mode.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 3: Agent Steering and Rules Configuration**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 3: Agent Steering and Rules Configuration` — the `.kiro/steering/` directory as a persistent context source, the Kiro context injector as the delivery mechanism, and the agent as the consumer.
2. Separate control-plane decisions (which steering files to create, scoping rules) from data-plane execution (file reads and context injection at session start).
3. Capture input contracts: markdown files in `.kiro/steering/`; output: augmented system prompt for every agent interaction.
4. Trace state transitions: no steering → steering files created → steering loaded at session start → agent behavior reflects rules.
5. Identify extension hooks: inclusion patterns for file-scoped rules, numeric prefixes for priority ordering.
6. Map ownership boundaries: team leads own `00-project.md` and `03-security.md`; individual developers own feature-specific steering files.
7. Specify rollback paths: remove or rename a steering file to exclude it from context; use git revert for team-wide rollback.
8. Track observability signals: verify agent responses reflect steering rules by testing with rule-specific questions.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Steering granularity | one general project.md | multiple scoped files per concern | simplicity vs precision |
| Rule enforcement | informational guidance | explicit forbidden patterns | flexibility vs compliance |
| Versioning | committed to git | PR review required for changes | speed vs governance |
| Scoping | global rules only | file-pattern scoped rules | ease vs relevance |
| Team ownership | any developer edits | designated maintainer with review | velocity vs consistency |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| steering not loaded | agent ignores known rules | session not restarted after adding files | reopen workspace to trigger re-load |
| conflicting rules | inconsistent agent output | two steering files with contradicting guidance | audit files for conflicts; use numeric prefix to set explicit priority |
| overly broad rules | agent refuses valid patterns | steering file uses absolute prohibition on useful patterns | rewrite rules as guidance with explicit exceptions |
| stale steering | agent applies outdated tech stack choices | steering not updated after refactor | add a quarterly steering review to the team's engineering calendar |
| rule explosion | too many steering files slow context loading | fine-grained file-per-rule authoring | consolidate related rules into thematic files |
| secret leakage in steering | sensitive values committed to git | developer pasted credentials into steering file | scan steering files with secret detection in CI |

### Implementation Runbook

1. Create the `.kiro/steering/` directory and add it to the git-tracked files.
2. Write `00-project.md` with the technology stack, key decisions, and forbidden patterns.
3. Write `01-coding-style.md` with language-specific style conventions for the primary language.
4. Write `02-testing.md` with the testing framework, naming conventions, and coverage targets.
5. Write `03-security.md` with authentication requirements, input validation policies, and dependency rules.
6. Reopen the workspace to trigger steering file loading.
7. Verify each steering file by asking a targeted question that requires knowledge of that file's rules.
8. Commit all steering files to version control with a PR description explaining each file's purpose.
9. Add a CI lint step to check steering files for secret patterns and markdown syntax errors.

### Quality Gate Checklist

- [ ] steering files cover the four core domains: project context, coding style, testing, and security
- [ ] all steering files use plain markdown with no embedded secrets or credentials
- [ ] file-scoped rules use valid inclusion patterns tested against actual file paths
- [ ] priority ordering is explicit via numeric prefixes on filenames
- [ ] steering rules are verified by targeted agent questions before committing
- [ ] steering files are committed to version control with clear PR descriptions
- [ ] a CI step checks steering files for secret patterns
- [ ] a review process is defined for who can approve changes to security.md and project.md

### Source Alignment

- [Kiro Docs: Steering](https://kiro.dev/docs/steering)
- [Kiro Docs: Steering Files](https://kiro.dev/docs/steering/files)
- [Kiro Docs: Steering Scoping](https://kiro.dev/docs/steering/scoping)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

### Cross-Tutorial Connection Map

- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [Agents MD Tutorial](../agents-md-tutorial/)
- [Chapter 4: Autonomous Agent Mode](04-autonomous-agent-mode.md)

### Advanced Practice Exercises

1. Write a complete four-file steering setup (project, style, testing, security) for a real project and verify each file's rules with targeted agent questions.
2. Create a file-scoped steering file for the `src/api/` directory and confirm it does not affect agent behavior in `src/models/`.
3. Simulate a steering conflict by writing two files with contradicting rules and observe the agent's behavior; then resolve the conflict with explicit priority ordering.
4. Add a GitHub Actions step that runs `gitleaks` or `trufflehog` against the `.kiro/steering/` directory on every PR.
5. Write a steering update proposal PR that changes a security rule and practice the review and approval workflow.

### Review Questions

1. What is the difference between a steering file and a chat prompt, and when should you use each?
2. How does Kiro determine the priority order when two steering files have conflicting rules?
3. What tradeoff did you make between steering granularity and context loading performance?
4. How would you recover if a steering file was accidentally committed with an API key?
5. What governance process should control changes to the security steering file in a team environment?

### Scenario Playbook 1: Steering - Rules Not Loaded After Adding Files

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent ignores steering rules despite `.kiro/steering/` containing valid markdown files
- initial hypothesis: the workspace session was not restarted after adding the steering files
- immediate action: close and reopen the Kiro workspace to trigger steering file re-loading
- engineering control: add a note to the team onboarding guide that workspace restart is required after steering changes
- verification target: agent responds with steering-aligned content when asked a targeted rule question
- rollback trigger: if restarting does not load steering, check for markdown syntax errors in the steering files
- communication step: document the restart requirement in the project's Kiro setup README section
- learning capture: request a Kiro feature for hot-reloading steering files without workspace restart

### Scenario Playbook 2: Steering - Conflicting Rules Between Files

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent produces inconsistent output because two steering files have contradicting guidance
- initial hypothesis: identify the specific rule conflict by reviewing all steering files for overlapping topics
- immediate action: temporarily disable the lower-priority file by renaming it with a `.disabled` extension
- engineering control: audit all steering files for topic overlap and consolidate conflicting rules into a single file
- verification target: agent consistently applies the intended rule with the conflict file disabled
- rollback trigger: if the conflict resolution introduces new inconsistencies, split into more narrowly scoped files
- communication step: document the conflict resolution decision in the PR that updates the steering files
- learning capture: add a steering file review checklist that flags topic overlap during PR review

### Scenario Playbook 3: Steering - Secret Committed to Steering File

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: a developer pasted a real API key or database password into a steering file and committed it
- initial hypothesis: confirm the secret is present by running gitleaks against the repository history
- immediate action: immediately revoke the exposed credential at the issuing service; do not wait for git history cleanup
- engineering control: use `git filter-branch` or BFG Repo Cleaner to remove the secret from git history, then force-push
- verification target: gitleaks scan reports zero secrets in `.kiro/steering/` after history cleanup
- rollback trigger: if history rewrite fails, mark the repository as compromised and rotate all project credentials
- communication step: notify the security team and affected service owners of the exposure within one hour
- learning capture: add a pre-commit hook that runs secret detection on `.kiro/steering/` before allowing commits

### Scenario Playbook 4: Steering - Stale Technology Stack After Refactor

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent recommends patterns from the old tech stack because project.md was not updated after a framework migration
- initial hypothesis: compare the current package.json and import statements against the technology stack in project.md
- immediate action: update project.md with the new framework and remove all references to the deprecated stack
- engineering control: add a steering review to the definition of done for major refactoring tasks
- verification target: agent recommends only the new framework's patterns after project.md is updated
- rollback trigger: if the update causes agent confusion, create a migration note section in project.md explaining the transition
- communication step: announce the project.md update in the team channel and ask members to restart their Kiro workspaces
- learning capture: add "update project.md" as a required step in the refactoring PR checklist

### Scenario Playbook 5: Steering - Overly Broad Security Rules Breaking Valid Patterns

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent refuses to generate valid code patterns because security.md uses absolute prohibitions that are too broad
- initial hypothesis: identify the specific rule that is blocking valid patterns and test with a targeted prompt
- immediate action: rewrite the prohibition as a conditional rule with explicit exceptions for the valid patterns
- engineering control: review all absolute prohibitions in security.md and add exception clauses where appropriate
- verification target: agent generates valid code patterns while still respecting the underlying security intent
- rollback trigger: if rule rewriting introduces security gaps, escalate to a security team review before committing
- communication step: document the rule refinement and its rationale in the security.md commit message
- learning capture: add a rule-testing protocol to the steering governance process: test each new rule with both valid and invalid code examples

## What Problem Does This Solve?

Without persistent project context, every Kiro session starts from scratch. Developers repeat the same stack choices, style preferences, and policy constraints in every chat prompt, and new team members have no way to discover what the AI has been told to do. Kiro's steering system solves this by storing project rules in version-controlled markdown files that are automatically injected into every agent interaction.

In practical terms, this chapter helps you avoid three common failures:

- agents generating code that contradicts established team conventions because the rules were never encoded
- inconsistent AI behavior across team members because each person prompts differently
- policy drift where security rules agreed upon in a meeting never make it into the AI's working context

After working through this chapter, you should be able to treat the `.kiro/steering/` directory as the authoritative source of your team's AI operating rules, reviewed and version-controlled like any other engineering artifact.

## How it Works Under the Hood

Under the hood, `Chapter 3: Agent Steering and Rules Configuration` follows a repeatable control path:

1. **Directory scan**: at workspace open, Kiro scans `.kiro/steering/` and loads all `.md` files in alphabetical order.
2. **Scoping evaluation**: for each file, Kiro checks the `applies_to` frontmatter against the current file context.
3. **Context injection**: active steering file content is prepended to the system prompt for every agent interaction.
4. **Priority resolution**: files with lower numeric prefixes take precedence when content conflicts.
5. **Session persistence**: steering context persists for the entire workspace session without re-loading on each message.
6. **Operational telemetry**: Kiro logs which steering files were loaded and their total character count for debugging.

When debugging steering issues, verify each stage: files exist, scoping matches, context is injected, and agent responses reflect the rules.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Docs: Steering](https://kiro.dev/docs/steering)
  Why it matters: the authoritative reference for the steering directory structure and file format.
- [Kiro Docs: Steering Files](https://kiro.dev/docs/steering/files)
  Why it matters: documents the frontmatter options including `applies_to` scoping patterns.
- [Kiro Docs: Steering Scoping](https://kiro.dev/docs/steering/scoping)
  Why it matters: explains how Kiro matches file-pattern rules against the current active file in the editor.
- [Kiro Repository](https://github.com/kirodotdev/Kiro)
  Why it matters: source of community-contributed steering file examples and issue tracking for steering bugs.

Suggested trace strategy:
- check the steering docs for the exact frontmatter schema before writing `applies_to` patterns
- test each steering file with a targeted question immediately after creation to confirm loading

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Spec-Driven Development Workflow](02-spec-driven-development-workflow.md)
- [Next Chapter: Chapter 4: Autonomous Agent Mode](04-autonomous-agent-mode.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
