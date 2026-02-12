---
layout: default
title: "Chapter 3: Providers and Model Routing"
nav_order: 3
parent: Goose Tutorial
---

# Chapter 3: Providers and Model Routing

This chapter focuses on selecting and configuring model providers for reliability, cost, and performance.

## Learning Goals

- compare provider categories in Goose
- configure provider credentials and model selection paths
- avoid common routing and rate-limit pitfalls
- standardize provider settings for team usage

## Provider Categories

| Category | Examples | Notes |
|:---------|:---------|:------|
| API providers | Anthropic, OpenAI, Groq, OpenRouter, xAI | best for direct programmatic control |
| cloud platform providers | Bedrock, Vertex AI, Databricks | enterprise policy alignment |
| local/compatible providers | Ollama, Docker Model Runner, LiteLLM | local privacy and custom routing |
| CLI pass-through providers | Claude Code, Codex CLI, Cursor Agent, Gemini CLI | can reuse existing subscriptions |

## Configuration Workflow

1. run `goose configure`
2. choose provider and authentication flow
3. select a model with tool-calling support
4. validate in a short task before long sessions

## Routing Stability Tips

- start with one default model before adding many alternatives
- use fallback strategy only after baseline behavior is stable
- keep provider credentials scoped and rotated
- document allowed providers in team onboarding docs

## Rate Limit and Failure Management

| Issue | Prevention |
|:------|:-----------|
| intermittent API failures | choose providers with retry-aware infrastructure |
| unstable model performance | pin known-good models for production tasks |
| auth drift across machines | standardize env var and secret manager strategy |

## Source References

- [Supported LLM Providers](https://block.github.io/goose/docs/getting-started/providers)
- [CLI Providers Guide](https://block.github.io/goose/docs/guides/cli-providers)
- [Rate Limits Guide](https://block.github.io/goose/docs/guides/handling-llm-rate-limits-with-goose)

## Summary

You now know how to route Goose through the right provider and model setup for your constraints.

Next: [Chapter 4: Permissions and Tool Governance](04-permissions-and-tool-governance.md)
