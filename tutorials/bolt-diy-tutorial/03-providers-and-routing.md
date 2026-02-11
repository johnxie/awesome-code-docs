---
layout: default
title: "Chapter 3: Providers and Model Routing"
nav_order: 3
parent: Bolt.diy Tutorial
---

# Chapter 3: Providers and Model Routing

bolt.diy's biggest advantage is provider flexibility. This chapter shows how to turn that flexibility into a controlled routing policy.

## Current Provider Surface

Upstream project docs describe support for many cloud and local providers, including OpenAI, Anthropic, Gemini, OpenRouter, Bedrock, local engines (for example Ollama/LM Studio), and more.

That breadth is useful only if you define:

- a primary provider strategy
- a fallback chain
- task-class routing rules
- cost and latency boundaries

## Routing as Policy, Not Preference

Avoid ad-hoc switching from UI alone. Use a policy table.

| Task Class | Primary | Fallback 1 | Fallback 2 | Notes |
|:-----------|:--------|:-----------|:-----------|:------|
| small scaffolding | low-latency model | medium model | local model | optimize for speed |
| architecture decisions | high-reasoning model | second high-reasoning model | medium model | quality over speed |
| privacy-sensitive tasks | local/self-hosted model | private gateway model | none | avoid external egress when required |
| high-volume batch edits | cost-efficient model | mid-cost model | local model | enforce spend caps |

## Minimum Routing Configuration

At a minimum, define these values per environment:

- default provider/model
- allowed provider list
- forbidden provider list (if compliance requires)
- fallback order
- timeout and retry limits
- budget cap per task/session

## Credential Management Baseline

### Development

- allow UI-assisted key setup for quick experimentation
- keep local secrets out of Git
- avoid sharing personal API keys across team accounts

### Staging/Production

- inject provider credentials from secret manager
- rotate keys on a fixed schedule
- separate read-only and privileged environment credentials

## Common Routing Failure Modes

### 1) Inconsistent results across providers

Different providers may follow tool and formatting instructions differently.

Mitigation:

- enforce stricter prompt contracts
- normalize output expectations in orchestration layer
- route sensitive tasks to stable high-performing defaults

### 2) Hidden cost spikes

Switching to stronger models without guardrails can silently increase spend.

Mitigation:

- per-task budget cap
- visible usage accounting per session
- periodic usage review by task type

### 3) Broken fallback logic

Fallback can fail if secondary provider config is incomplete.

Mitigation:

- scheduled fallback health checks
- failover drills in non-production environment
- keep a tested emergency fallback profile

## Recommended Team Profiles

| Profile | Purpose | Default Settings |
|:--------|:--------|:-----------------|
| `dev-fast` | everyday iteration | low-latency model + cheap fallback |
| `review-safe` | risky or wide-scope refactors | stronger reasoning model + strict approvals |
| `private-mode` | sensitive code/data | local/self-hosted providers only |
| `batch-cost` | repetitive bulk work | cost-optimized model + hard caps |

## Example Environment Strategy

```bash
# Example names only; use your real variables and secret manager
PRIMARY_PROVIDER=openrouter
PRIMARY_MODEL=...
FALLBACK_PROVIDER=anthropic
FALLBACK_MODEL=...
TERTIARY_PROVIDER=ollama
TERTIARY_MODEL=...
TASK_BUDGET_USD=3.00
```

Use this as conceptual structure, not a hard-coded upstream contract.

## Routing Readiness Checklist

- default and fallback providers are documented
- each provider path is smoke-tested weekly
- budget limits are visible to operators
- error categories are captured in logs
- incident runbook includes provider outage steps

## Chapter Summary

You now have a provider-routing governance model that covers:

- task-class model selection
- fallback resilience
- spend controls
- credential and compliance boundaries

Next: [Chapter 4: Prompt-to-App Workflow](04-prompt-to-app-workflow.md)
