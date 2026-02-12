---
layout: default
title: "Chapter 6: Headless Mode and CI Automation"
nav_order: 6
parent: Gemini CLI Tutorial
---

# Chapter 6: Headless Mode and CI Automation

This chapter shows how to run Gemini CLI in deterministic automation loops.

## Learning Goals

- run non-interactive prompts in scripts and CI jobs
- choose between text, JSON, and streaming JSON outputs
- parse response structures reliably for downstream steps
- integrate Gemini CLI with GitHub workflow automation

## Headless Patterns

### Basic text automation

```bash
gemini -p "Generate a changelog for this diff"
```

### Structured JSON output

```bash
gemini -p "Summarize test failures" --output-format json
```

### Event stream mode

```bash
gemini -p "Run release checklist" --output-format stream-json
```

## CI Integration Notes

- use explicit prompts with strict output contracts
- parse machine-readable output with resilient tooling
- fail fast on non-zero exit codes and invalid JSON

## Source References

- [Headless Mode Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md)
- [CLI Reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/cli-reference.md)
- [GitHub Action Integration](https://github.com/google-github-actions/run-gemini-cli)

## Summary

You now have practical patterns for scriptable and CI-safe Gemini CLI execution.

Next: [Chapter 7: Sandboxing, Security, and Troubleshooting](07-sandboxing-security-and-troubleshooting.md)
