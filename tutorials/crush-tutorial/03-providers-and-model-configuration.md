---
layout: default
title: "Chapter 3: Providers and Model Configuration"
nav_order: 3
parent: Crush Tutorial
---

# Chapter 3: Providers and Model Configuration

This chapter covers provider setup, model routing, and custom provider definitions.

## Learning Goals

- configure supported providers via environment variables
- define custom OpenAI-compatible and Anthropic-compatible providers
- tune model metadata for stable coding behavior
- avoid provider drift across team environments

## Provider Baseline

Crush supports many providers directly via environment variables, including:

- Anthropic
- OpenAI
- Vercel AI Gateway
- Gemini
- OpenRouter
- Groq
- Vertex AI
- Amazon Bedrock

## Custom Provider Pattern

For non-default endpoints, define provider objects in config using:

- `type: openai-compat` for OpenAI-compatible APIs
- `type: anthropic` for Anthropic-compatible APIs

Include model metadata such as context window and token defaults when available.

## Routing Stability Tips

| Risk | Mitigation |
|:-----|:-----------|
| inconsistent responses between machines | share a team config baseline |
| accidental provider fallback | pin active provider/model explicitly |
| cost surprises | capture token economics in model metadata |

## Source References

- [Crush README: Getting Started](https://github.com/charmbracelet/crush/blob/main/README.md#getting-started)
- [Crush README: Custom Providers](https://github.com/charmbracelet/crush/blob/main/README.md#custom-providers)
- [Crush schema](https://github.com/charmbracelet/crush/blob/main/schema.json)

## Summary

You now have a predictable strategy for provider selection and model routing in Crush.

Next: [Chapter 4: Permissions and Tool Controls](04-permissions-and-tool-controls.md)
