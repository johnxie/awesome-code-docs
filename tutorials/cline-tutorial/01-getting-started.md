---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Cline Tutorial
---

# Chapter 1: Getting Started

This chapter gets Cline installed and configured for safe day-to-day engineering use.

## Objectives

By the end, you will have:

1. Cline installed in VS Code-compatible environment
2. a working provider/model configuration
3. a first task that exercises read, edit, command, and summary phases
4. a baseline safety policy for approvals

## Prerequisites

| Requirement | Why It Matters |
|:------------|:---------------|
| VS Code (or compatible editor) | Cline runs as an editor extension |
| API key for at least one provider | model-backed planning and tool use |
| sandbox repository | low-risk environment for calibration |
| test/lint command in repo | deterministic validation signal |

## Install Flow

### Option A: VS Code Marketplace

1. Open Extensions panel.
2. Search for Cline.
3. Install and reload editor.

### Option B: Prebuilt extension package (team-managed)

Use this for internal distribution or controlled rollouts.

## Provider Setup

Cline supports multiple providers and local options. Start with one reliable model/provider pair before configuring advanced routing.

Recommended first-run approach:

- choose one strong default model
- keep approvals enabled for file edits and terminal commands
- disable risky automations until baseline is stable

## First Task (Deterministic)

Use a bounded prompt contract:

```text
Analyze src/auth/session.ts,
refactor one function for readability without changing behavior,
run npm test -- auth-session,
and summarize changed files and test results.
```

Success criteria:

- Cline proposes edits as reviewable diffs
- only expected files are modified
- command output is captured
- final summary maps changes to validation evidence

## Baseline Safety Settings

Before broader usage, set defaults:

- explicit approval required for commands with side effects
- explicit approval for file writes
- disable YOLO-style behavior by default
- require task summary before completion

## First-Run Health Checklist

| Area | Check | Pass Signal |
|:-----|:------|:------------|
| Install | extension activates correctly | Cline panel opens without errors |
| Provider | API call succeeds | first prompt returns actionable response |
| Diff flow | write proposals are reviewable | file patch appears before apply |
| Command flow | terminal execution works | output attached to task timeline |
| Context flow | file understanding is accurate | summary references real code facts |

## Common Setup Failures

### Provider authentication failures

- verify API key placement and provider selection
- test with one provider first
- avoid mixing multiple misconfigured profiles at startup

### Command execution confusion

- ensure repository has canonical commands (`npm test`, `pnpm test`, etc.)
- explicitly state the command in prompts
- avoid ambiguous "run tests" instructions on first day

### Noisy outputs

- tighten task scope to one file/module
- include non-goals in prompt
- require strict summary format

## Team Onboarding Template

When onboarding multiple engineers, standardize:

1. default provider/model
2. required approval policy
3. prompt template
4. required validation commands per repo
5. escalation path for unsafe proposals

This prevents inconsistent behavior across developers.

## Chapter Summary

You now have a working Cline baseline with:

- installation complete
- provider configuration validated
- first deterministic task executed
- safety settings ready for deeper workflows

Next: [Chapter 2: Agent Workflow](02-agent-workflow.md)
