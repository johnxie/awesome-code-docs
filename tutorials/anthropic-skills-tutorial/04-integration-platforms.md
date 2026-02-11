---
layout: default
title: "Chapter 4: Integration Platforms"
nav_order: 4
parent: Anthropic Skills Tutorial
---

# Chapter 4: Integration Platforms

The same skill package can be used across multiple surfaces, but deployment and governance expectations differ.

## Claude Code

Claude Code is strong for engineering and file-centric workflows.

From the official skills repository, a common setup is:

```bash
/plugin marketplace add anthropics/skills
/plugin install example-skills@anthropic-agent-skills
```

Operational guidance:

- Keep skill repos versioned and pinned.
- Prefer local scripts for deterministic steps.
- Enforce repository-level review on `SKILL.md` changes.

## Claude.ai

Claude.ai is ideal for interactive drafting and team collaboration.

Use it when:

- humans need to iterate on outputs quickly
- file upload context is part of the workflow
- you want lower-friction skill adoption for non-engineers

Guardrail recommendation: keep a canonical output template in the skill so generated artifacts remain comparable.

## Claude API

API integration gives maximal control for enterprise systems.

Typical pattern:

1. Load skill instructions as controlled context.
2. Inject request-specific payload.
3. Validate output against schema.
4. Store run metadata for auditing.

Pseudo-flow:

```text
request -> select skill -> build prompt context -> generate -> validate -> persist
```

## Cross-Platform Compatibility Strategy

| Concern | Claude Code | Claude.ai | Claude API |
|:--------|:------------|:----------|:-----------|
| Local file/scripts | Strong | Limited | App-controlled |
| Governance controls | Git + review | Workspace policies | Full policy engine |
| Structured validation | Medium | Medium | Strong |
| Automation depth | High | Medium | Highest |

## Integration Pitfalls

- Reusing one skill unchanged across radically different environments
- Assuming runtime-specific tools exist everywhere
- Failing to log skill version with each generated artifact

## Summary

You can now choose the right runtime surface and adjust operating controls per platform.

Next: [Chapter 5: Production Skills](05-production-skills.md)
