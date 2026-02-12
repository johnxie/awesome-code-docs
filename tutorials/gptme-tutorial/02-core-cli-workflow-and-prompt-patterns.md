---
layout: default
title: "Chapter 2: Core CLI Workflow and Prompt Patterns"
nav_order: 2
parent: gptme Tutorial
---

# Chapter 2: Core CLI Workflow and Prompt Patterns

gptme supports direct prompt invocation, chained prompts, and resumed sessions for iterative development.

## Workflow Patterns

| Pattern | Example |
|:--------|:--------|
| interactive | `gptme` |
| single prompt | `gptme "summarize this" README.md` |
| chained prompts | `gptme "make a change" - "test it" - "commit it"` |
| resume session | `gptme -r` |

## Practical Guidance

Use chained prompts to enforce staged execution (change -> test -> commit) instead of single broad prompts.

## Source References

- [gptme README usage examples](https://github.com/gptme/gptme/blob/master/README.md)
- [CLI entrypoint options](https://github.com/gptme/gptme/blob/master/gptme/cli/main.py)

## Summary

You now know how to structure repeatable prompt flows and resume long-running conversations.

Next: [Chapter 3: Tooling and Local Execution Boundaries](03-tooling-and-local-execution-boundaries.md)
