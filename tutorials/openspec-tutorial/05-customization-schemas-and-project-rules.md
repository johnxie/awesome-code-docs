---
layout: default
title: "Chapter 5: Customization, Schemas, and Project Rules"
nav_order: 5
parent: OpenSpec Tutorial
---

# Chapter 5: Customization, Schemas, and Project Rules

OpenSpec can be tailored to your engineering environment through configuration and schema controls.

## Learning Goals

- use `openspec/config.yaml` for project defaults and rules
- understand schema precedence and artifact IDs
- avoid over-customization that breaks portability

## Example Project Config

```yaml
schema: spec-driven

context: |
  Tech stack: TypeScript, React, Node.js
  Testing: Vitest and Playwright

rules:
  proposal:
    - Include rollback plan for risky changes
  specs:
    - Use Given/When/Then in scenarios
```

## Schema Precedence

1. CLI `--schema`
2. change-level metadata
3. project config default
4. built-in default schema

## Customization Strategy

| Layer | Use For |
|:------|:--------|
| context | stack facts and non-obvious constraints |
| rules | artifact-specific quality constraints |
| custom schemas | domain-specific artifact graphs |

## Source References

- [Customization Guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)
- [CLI Schema Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)
- [OPSX Workflow Config Section](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)

## Summary

You now know how to shape OpenSpec behavior while keeping workflows maintainable across teams.

Next: [Chapter 6: Tool Integrations and Multi-Agent Portability](06-tool-integrations-and-multi-agent-portability.md)
