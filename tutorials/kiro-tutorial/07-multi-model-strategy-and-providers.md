---
layout: default
title: "Chapter 7: Multi-Model Strategy and Providers"
nav_order: 7
parent: Kiro Tutorial
---

# Chapter 7: Multi-Model Strategy and Providers

Welcome to **Chapter 7: Multi-Model Strategy and Providers**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Kiro uses Claude Sonnet 4.0 and 3.7 by default and routes different task types to different model configurations. This chapter teaches you how to configure the model strategy for your team's workload profile.

## Learning Goals

- understand Kiro's default model routing between Claude Sonnet 4.0 and 3.7
- configure model preferences for different task categories
- understand the cost and latency tradeoffs between model tiers
- set up budget controls and usage monitoring
- plan model upgrades as new Claude versions become available

## Fast Start Checklist

1. open Kiro settings and navigate to the Model section
2. confirm the default model is Claude Sonnet 4.0
3. optionally override to Claude Sonnet 3.7 for faster or lower-cost interactive chat
4. set a daily token budget for cost control
5. review the model usage dashboard after a full session

## Default Model Configuration

Kiro ships with two default model profiles:

| Profile | Model | Best For |
|:--------|:------|:---------|
| Primary | Claude Sonnet 4.0 | autonomous agent tasks, spec generation, complex code synthesis |
| Fast | Claude Sonnet 3.7 | interactive chat, quick edits, explanation and Q&A |

Kiro automatically selects the appropriate model based on the interaction type. You can override this selection for specific use cases.

## Model Configuration in Settings

```json
{
  "models": {
    "primary": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-0",
      "maxTokens": 8192,
      "temperature": 0.1
    },
    "fast": {
      "provider": "anthropic",
      "model": "claude-sonnet-3-7",
      "maxTokens": 4096,
      "temperature": 0.2
    },
    "routing": {
      "specGeneration": "primary",
      "taskExecution": "primary",
      "interactiveChat": "fast",
      "hookActions": "fast",
      "codeExplanation": "fast"
    }
  }
}
```

## Claude Sonnet 4.0 vs. 3.7

| Capability | Claude Sonnet 4.0 | Claude Sonnet 3.7 |
|:-----------|:-----------------|:-----------------|
| Code synthesis quality | higher | good |
| Multi-step reasoning | stronger | capable |
| Response latency | moderate | faster |
| Cost per token | higher | lower |
| Context window | 200k tokens | 200k tokens |
| Best use case | spec generation, complex tasks | chat, quick edits |

## Task-to-Model Routing

Map task types to model profiles based on your team's cost and quality priorities:

```json
{
  "models": {
    "routing": {
      "specGeneration": "primary",       // requirements → design → tasks: quality matters most
      "taskExecution": "primary",        // autonomous agent: complex multi-step reasoning
      "codeReview": "primary",           // security and correctness review: quality matters
      "interactiveChat": "fast",         // quick Q&A and exploration: speed matters
      "hookActions": "fast",             // frequent event-driven actions: cost matters
      "codeExplanation": "fast",         // explaining existing code: speed and cost
      "documentationUpdate": "fast"      // doc updates: lower complexity
    }
  }
}
```

## Budget Controls

Set daily and monthly token budgets to prevent unexpected cost spikes:

```json
{
  "budget": {
    "daily": {
      "inputTokens": 500000,
      "outputTokens": 200000,
      "alertThreshold": 0.8,
      "action": "notify"
    },
    "monthly": {
      "inputTokens": 10000000,
      "outputTokens": 4000000,
      "alertThreshold": 0.9,
      "action": "restrict"
    }
  }
}
```

Budget actions:
- `notify`: send an alert to the chat panel when the threshold is reached
- `restrict`: switch all routing to the `fast` (lower-cost) model when the threshold is reached
- `pause`: stop all agent activity and require manual reset when the limit is reached

## Usage Monitoring

Track model usage in the Kiro dashboard:

```
# In the Chat panel:
> /usage

# Output:
Session token usage:
  Input: 47,832 tokens (Claude Sonnet 4.0: 31,200 | Claude Sonnet 3.7: 16,632)
  Output: 12,441 tokens (Claude Sonnet 4.0: 9,800 | Claude Sonnet 3.7: 2,641)
  Estimated cost: $0.43

Daily usage: 182,341 input / 48,902 output tokens (36% of daily budget)
```

## Cost Optimization Patterns

| Pattern | Description | Token Savings |
|:--------|:------------|:-------------|
| Route chat to fast model | use Sonnet 3.7 for all interactive chat | 30-50% reduction on chat costs |
| Scope task context | pass only relevant spec sections to agents | 20-40% reduction per task |
| Compress steering files | remove redundant rules from steering files | 5-15% reduction on base context |
| Limit hook frequency | use commit-level hooks instead of save-level | 60-80% reduction on hook costs |
| Batch spec generation | generate all spec documents in one call | 10-20% reduction vs. sequential calls |

## Preparing for Model Upgrades

When AWS releases a new Claude version in Kiro, follow this upgrade protocol:

1. review the release notes for the new model version
2. test spec generation on a sample feature spec with the new model
3. compare output quality against the previous model on the same spec
4. if quality is equal or better, update the `primary` routing to the new model
5. run the full test suite on an autonomous agent task using the new model
6. monitor token usage for the first week on the new model
7. update the model configuration in version control and notify the team

## Source References

- [Kiro Docs: Model Configuration](https://kiro.dev/docs/models)
- [Kiro Docs: Budget Controls](https://kiro.dev/docs/models/budget)
- [Anthropic Models Overview](https://docs.anthropic.com/en/docs/models-overview)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now know how to configure Kiro's model routing, set budget controls, monitor usage, and plan for model upgrades.

Next: [Chapter 8: Team Operations and Governance](08-team-operations-and-governance.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 7: Multi-Model Strategy and Providers**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 7: Multi-Model Strategy and Providers` — the model routing layer, the budget controller, and the provider API gateway.
2. Separate control-plane decisions (model selection, routing policy, budget limits) from data-plane execution (token generation, inference calls).
3. Capture input contracts: task type classification from interaction context; output: model-routed inference request and response.
4. Trace state transitions: task initiated → type classified → routing rule applied → model selected → request sent → response received → cost tracked.
5. Identify extension hooks: custom routing rules per task type, budget action policies, provider failover paths.
6. Map ownership boundaries: developers choose fast/primary preference; team leads set routing policy; finance owns budget limits.
7. Specify rollback paths: switch routing back to previous model; restore budget settings from version control.
8. Track observability signals: token consumption per model per task type, cost per session, budget threshold alerts, model latency distribution.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Model selection | Kiro defaults (Sonnet 4.0 primary) | explicit routing per task type | ease vs cost optimization |
| Budget controls | monthly soft cap with notification | daily hard cap with auto-restrict | flexibility vs cost certainty |
| Upgrade cadence | upgrade immediately on release | validation protocol before upgrade | speed vs quality assurance |
| Usage monitoring | check manually via /usage | automated daily usage reports | effort vs visibility |
| Cost allocation | project-level budget | per-developer or per-team budgets | simplicity vs granularity |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| budget overrun | unexpected high token usage | hooks or autonomous tasks using primary model at high frequency | audit routing config and redirect high-frequency actions to fast model |
| model quality regression | lower spec generation quality after upgrade | new model performs differently on the team's task profile | run quality benchmark before upgrading primary model |
| provider outage | 503 errors on model API calls | Anthropic service disruption | configure fallback model or degrade to interactive-only mode |
| token waste on large contexts | high input token counts for simple tasks | full codebase context sent for small tasks | scope context explicitly in task descriptions |
| routing misconfiguration | wrong model used for expensive tasks | misconfigured routing JSON | audit routing config and verify with /usage after changes |
| cost spike from hook frequency | daily budget hits threshold early | save-level hooks using primary model | switch hook routing to fast model and add conditions to reduce frequency |

### Implementation Runbook

1. Review the Kiro model documentation to understand the current Claude Sonnet 4.0 and 3.7 capability profiles.
2. Map your team's top five task types to the appropriate model tier based on quality vs. cost priority.
3. Configure the routing policy in Kiro settings or `.kiro/settings.json`.
4. Set a daily token budget with a notify action at 80% of the limit.
5. Run a full one-day session with the new configuration and review the `/usage` output.
6. Identify the three highest-cost task types and optimize their routing or context scope.
7. Set the monthly budget with a restrict action at 90% of the limit.
8. Document the model routing rationale in `.kiro/settings.json` comments for team transparency.
9. Schedule a quarterly model upgrade review to assess whether new Claude versions improve quality or reduce cost.

### Quality Gate Checklist

- [ ] routing policy is explicitly configured for at least five task types in settings
- [ ] daily and monthly token budgets are set with appropriate alert thresholds
- [ ] budget action for monthly limit is set to `restrict` or `pause` to prevent overruns
- [ ] `/usage` is reviewed after the first full day with the new routing configuration
- [ ] high-frequency hook actions are routed to the fast model
- [ ] a model upgrade validation protocol is documented before the first upgrade
- [ ] routing configuration is committed to version control with clear comments
- [ ] team members are informed of the routing policy and budget limits

### Source Alignment

- [Kiro Docs: Model Configuration](https://kiro.dev/docs/models)
- [Kiro Docs: Budget Controls](https://kiro.dev/docs/models/budget)
- [Kiro Docs: Usage Dashboard](https://kiro.dev/docs/models/usage)
- [Anthropic Models Overview](https://docs.anthropic.com/en/docs/models-overview)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

### Cross-Tutorial Connection Map

- [LiteLLM Tutorial](../litellm-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [OpenCode Tutorial](../opencode-tutorial/)
- [Cline Tutorial](../cline-tutorial/)
- [Chapter 8: Team Operations and Governance](08-team-operations-and-governance.md)

### Advanced Practice Exercises

1. Configure a complete routing policy for six task types and document the quality vs. cost rationale for each routing decision.
2. Run identical spec generation tasks with Sonnet 4.0 and Sonnet 3.7 and compare output quality in a structured evaluation table.
3. Simulate a budget overrun by setting a very low daily limit and observe the restrict action behavior; then restore the correct limit.
4. Build a model upgrade validation checklist for your team's specific task profile and run it against a hypothetical new Claude version.
5. Analyze one week of `/usage` output and identify the top three opportunities to reduce token consumption without reducing quality.

### Review Questions

1. Why does Kiro route spec generation to the primary (Sonnet 4.0) model rather than the fast model by default?
2. What is the difference between the `restrict` and `pause` budget actions, and when should you use each?
3. What tradeoff did you make between model quality and cost when routing hook actions to the fast model?
4. How would you validate that a new Claude model version is safe to use as the primary routing target for your team's spec generation tasks?
5. What conditions trigger an automatic routing switch in Kiro's budget control system?

### Scenario Playbook 1: Model Strategy - Budget Overrun from Hook Frequency

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: daily token budget alert fires at 9am because file:save hooks are consuming primary model tokens at high frequency
- initial hypothesis: hooks are routing to the primary model and activating on every TypeScript file save in a large codebase
- immediate action: switch all hook routing to the fast model and add file-pattern conditions to reduce activation rate
- engineering control: update the routing config to explicitly map `hookActions` to `fast` model
- verification target: token usage at end of day stays below 60% of the daily budget after routing change
- rollback trigger: if fast model produces lower-quality hook outputs that are actionable, add a flag for critical hooks to use primary
- communication step: notify the team of the routing change and explain the cost rationale
- learning capture: add hook routing as a required configuration step in the team's Kiro onboarding checklist

### Scenario Playbook 2: Model Strategy - Quality Regression After Upgrade

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: spec generation quality drops noticeably after the team upgraded to a new Claude version
- initial hypothesis: the new model has different default behaviors for EARS requirement parsing and design generation
- immediate action: revert the primary model routing to the previous version while the quality issue is investigated
- engineering control: run the quality benchmark suite on the new model version and document the delta
- verification target: benchmark scores for spec generation match or exceed the previous model version
- rollback trigger: if the new model cannot match previous quality after prompt adjustments, remain on the previous version
- communication step: share the benchmark results with the team and the model upgrade status
- learning capture: add a quality benchmark run as a mandatory step before any future model version upgrade

### Scenario Playbook 3: Model Strategy - Provider Outage

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: Anthropic API returns 503 errors causing all Kiro model calls to fail
- initial hypothesis: the Anthropic service is experiencing an outage affecting the Claude Sonnet endpoints
- immediate action: check the Anthropic status page and switch Kiro to interactive-only mode for in-flight autonomous tasks
- engineering control: configure a fallback model in Kiro settings pointing to an alternative provider if available
- verification target: team can continue interactive chat in degraded mode while the outage is active
- rollback trigger: restore full model routing once Anthropic reports the incident resolved
- communication step: notify the team of the outage status and expected recovery time from the Anthropic status page
- learning capture: add provider outage response steps to the team's Kiro incident runbook

### Scenario Playbook 4: Model Strategy - Token Waste on Large Contexts

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: `/usage` shows extremely high input token counts for tasks that should be simple
- initial hypothesis: the agent is loading the full codebase context for tasks that only require a single file or module
- immediate action: add explicit context constraints to the task descriptions in tasks.md: "only read files in src/auth/"
- engineering control: update the spec generation prompt template to include a "context scope" field for each task
- verification target: input token count per task decreases by at least 30% after scope constraints are applied
- rollback trigger: if scope constraints cause the agent to miss necessary context, expand the scope incrementally
- communication step: share the context scoping pattern with the team as a best practice in the Kiro usage guide
- learning capture: add a context scope field to the tasks.md template and document the expected files per task type

### Scenario Playbook 5: Model Strategy - Routing Misconfiguration

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: interactive chat is using the primary (Sonnet 4.0) model despite routing being configured for fast model
- initial hypothesis: the routing configuration in settings.json has a syntax error or the key name does not match Kiro's expected format
- immediate action: validate the settings.json against the Kiro settings schema and fix any key name mismatches
- engineering control: add a JSON schema validation step to the CI pipeline for `.kiro/settings.json`
- verification target: `/usage` confirms interactive chat is routed to Sonnet 3.7 after the configuration fix
- rollback trigger: if schema validation is not feasible, revert settings.json to the last known good commit
- communication step: share the corrected settings.json format with the team and update the configuration docs
- learning capture: add a settings.json validation step to the Kiro onboarding checklist

## What Problem Does This Solve?

Most agentic coding tools treat model selection as a binary choice. Kiro's multi-model routing strategy recognizes that different task types have fundamentally different quality and cost requirements. Spec generation demands the highest-quality reasoning; interactive chat demands the lowest latency. Routing these to the same model either wastes money on fast interactions or underserves the tasks that matter most.

In practical terms, this chapter helps you avoid three common failures:

- paying primary-model prices for every lint check, code explanation, and quick question
- using a fast model for spec generation and getting design documents that miss key architectural considerations
- running out of daily token budget before the high-value autonomous tasks run

After working through this chapter, you should be able to treat model routing as a cost-quality optimization policy that is explicit, versioned, and tuned to your team's actual workload distribution.

## How it Works Under the Hood

Under the hood, `Chapter 7: Multi-Model Strategy and Providers` follows a repeatable control path:

1. **Task type classification**: Kiro inspects the interaction type (chat, spec generation, hook action, etc.) to classify the task.
2. **Routing rule lookup**: the routing policy in settings is consulted to select the model profile for the task type.
3. **Budget check**: before dispatching, Kiro checks the current usage against the configured budget limits.
4. **Model API call**: Kiro sends the inference request to the Anthropic API endpoint for the selected model.
5. **Response tracking**: the token counts from the API response are recorded against the session and daily budgets.
6. **Usage aggregation**: the dashboard aggregates usage by model, task type, and time window for monitoring.

When debugging cost or quality issues, trace this sequence from task classification through budget tracking to identify where the routing or consumption is diverging from expectations.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Docs: Model Configuration](https://kiro.dev/docs/models)
  Why it matters: the primary reference for routing configuration format and available model identifiers.
- [Kiro Docs: Budget Controls](https://kiro.dev/docs/models/budget)
  Why it matters: documents the exact budget action behaviors and threshold configuration options.
- [Anthropic Models Overview](https://docs.anthropic.com/en/docs/models-overview)
  Why it matters: the canonical reference for Claude model capabilities, context windows, and pricing tiers.
- [Kiro Repository](https://github.com/kirodotdev/Kiro)
  Why it matters: source for model configuration schema and community discussions on routing strategies.

Suggested trace strategy:
- check the Anthropic models page before configuring routing to confirm the current model identifier strings
- run `/usage` after each configuration change to confirm routing is working as intended

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Hooks and Automation](06-hooks-and-automation.md)
- [Next Chapter: Chapter 8: Team Operations and Governance](08-team-operations-and-governance.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
