---
layout: default
title: "Chapter 6: Programmatic and Non-Interactive Modes"
nav_order: 6
parent: Mistral Vibe Tutorial
---

# Chapter 6: Programmatic and Non-Interactive Modes

Vibe can run non-interactively for scripted workflows with bounded turns/cost and structured output.

## Programmatic Example

```bash
vibe --prompt "Analyze security risks in src/" --max-turns 5 --max-price 1.0 --output json
```

## Automation Controls

- `--max-turns` for deterministic upper bounds
- `--max-price` for cost control
- `--output` for machine-readable integration

## Source References

- [Mistral Vibe README: programmatic mode](https://github.com/mistralai/mistral-vibe/blob/main/README.md)

## Summary

You now understand how to use Vibe for script-friendly and CI-ready tasks.

Next: [Chapter 7: ACP and Editor Integrations](07-acp-and-editor-integrations.md)
