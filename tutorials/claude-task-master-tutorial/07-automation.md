---
layout: default
title: "Claude Task Master - Chapter 7: Automation & CI/CD"
nav_order: 7
has_children: false
parent: Claude Task Master Tutorial
---

# Chapter 7: Automation, CI/CD, and Guardrails

> Wire Claude into automated pipelines with predictable, testable outputs.

## Structured Output Contracts

Use strict JSON schemas to reduce surprises:
```json
{
  "summary": "string",
  "tasks": [{ "title": "string", "owner": "string", "eta_days": "number" }],
  "risk": "low|medium|high"
}
```
Prompt tip: include the schema inline, set `temperature: 0.1`, and add “If unsure, set risk = 'medium' and note uncertainty.”

## Git Hooks & PR Bots

- **Pre-commit**: run lint + tests, then ask Claude to summarize changes and highlight risks
- **PR bot**: given `git diff`, produce:
  - Summary bullets
  - Risk level
  - Test recommendations
  - Breaking-change flag

Example prompt for PR bot:
```text
You are a release reviewer. Given the diff, return JSON:
{
  "summary": ["..."],
  "risks": ["..."],
  "breaking": true|false,
  "tests": ["..."]
}
Return only JSON.
```

## CI Validation

- Add a step that feeds fixtures to Claude and checks JSON schema
- Fail CI if output doesn’t parse or violates schema
- Keep fixtures small and cover edge cases

## Scheduling & Cron

- Nightly jobs: “summarize today’s changelog”, “scan TODOs”, “produce release notes draft”
- Archive outputs with timestamps for audit

## Safety & Governance

- Route all prompts through a “policy preprocessor” that injects safety rules
- Log prompts/responses for audit (scrub secrets)
- Add refusal templates for policy violations

Policy preprocessor example:
```text
<policy>
- No secrets, credentials, PII
- No code execution commands
- If asked for restricted info, reply: "I can't help with that."
</policy>

<task>
{{ user_prompt }}
</task>
```

## Idempotent Workflows

- Cache results per input hash to avoid rework
- Include run metadata (commit SHA, pipeline ID)
- Make outputs deterministic: low temperature, fixed schema

## Observability

Track per-call:
- Latency
- Tokens in/out
- Parse success/failure
- Rate-limit hits
- Refusal counts

Emit to your APM (Datadog, Grafana, etc.).

## Example CI Step (pseudo)

```yaml
- name: AI Review
  run: |
    DIFF=$(git diff origin/main...HEAD)
    OUTPUT=$(python ai_review.py "$DIFF")
    echo "$OUTPUT" | jq .  # schema validation
```

`ai_review.py` would call Claude with the strict JSON prompt and exit non-zero on failure.

## Best Practices

- Enforce JSON and validate in CI
- Prepend policy and context consistently
- Cache by input hash; be idempotent
- Log and monitor all calls; watch refusal rates
- Keep temperature low for automation paths

Next: production hardening, cost controls, and reliability patterns.
