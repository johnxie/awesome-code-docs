---
layout: default
title: "Chapter 3: Authentication and Model Access Strategy"
nav_order: 3
parent: Gemini CLI Tutorial
---

# Chapter 3: Authentication and Model Access Strategy

This chapter compares available auth paths and helps you choose model-access strategy by team constraints.

## Learning Goals

- choose OAuth, API key, or Vertex AI auth path correctly
- understand model-routing precedence and controls
- avoid common enterprise auth misconfiguration
- align auth choice with usage, compliance, and quota needs

## Authentication Paths

### Google OAuth

Best for individual developers and fast setup.

```bash
gemini
```

### Gemini API Key

Best for explicit key-based control.

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
gemini
```

### Vertex AI

Best for enterprise billing/compliance integration.

```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
export GOOGLE_GENAI_USE_VERTEXAI=true
gemini
```

## Model Strategy Notes

- set default model for predictable behavior
- override per run for targeted cost/performance decisions
- verify routing precedence when multiple settings sources exist

## Source References

- [README Authentication Options](https://github.com/google-gemini/gemini-cli/blob/main/README.md#-authentication-options)
- [Authentication Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/authentication.md)
- [Model Routing Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model-routing.md)

## Summary

You now have a clear and repeatable auth/model-access strategy.

Next: [Chapter 4: Settings, Context, and Custom Commands](04-settings-context-and-custom-commands.md)
