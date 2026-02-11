---
layout: default
title: "Chapter 3: Providers and Model Routing"
nav_order: 3
parent: Bolt.diy Tutorial
---

# Chapter 3: Providers and Model Routing

A major bolt.diy advantage is provider flexibility across cloud and local models.

## Provider Model

The project supports a large set of providers (OpenAI, Anthropic, Google-family integrations, OpenRouter, Ollama, and others), with configuration managed through environment variables and settings UI.

## Configuration Patterns

- **Production/CI**: manage keys in environment variables and secret stores
- **Interactive local use**: settings UI for rapid provider switching
- **Hybrid**: cloud for complex tasks, local for low-cost/private iterations

## Routing Strategy

Use workload-based routing:

- fast/cheap models for scaffolding and refactors
- stronger models for architecture decisions and tricky debugging
- local models when privacy or offline constraints dominate

## Guardrails

| Risk | Control |
|:-----|:--------|
| leaked keys | no hardcoded keys, secrets scanning |
| wrong provider fallback | explicit default model policy |
| cost spikes | per-session token budget and alerts |

## Summary

You can now configure provider routing as a deliberate engineering policy instead of ad hoc toggling.

Next: [Chapter 4: Prompt-to-App Workflow](04-prompt-to-app-workflow.md)
