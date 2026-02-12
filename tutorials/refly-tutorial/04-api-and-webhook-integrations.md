---
layout: default
title: "Chapter 4: API and Webhook Integrations"
nav_order: 4
parent: Refly Tutorial
---

# Chapter 4: API and Webhook Integrations

This chapter covers the two primary operational integration surfaces for Refly workflows.

## Learning Goals

- authenticate and call workflow APIs correctly
- track execution state and retrieve outputs reliably
- enable webhook-driven triggers with variable payloads
- choose API vs webhook based on control requirements

## API Integration Pattern

| Step | Endpoint Family | Outcome |
|:-----|:----------------|:--------|
| trigger run | `POST /openapi/workflow/{canvasId}/run` | receive execution ID |
| check status | `GET /openapi/workflow/{executionId}/status` | monitor state transitions |
| fetch output | `GET /openapi/workflow/{executionId}/output` | collect artifacts/results |
| abort if needed | `POST /openapi/workflow/{executionId}/abort` | controlled interruption |

## Webhook Usage Pattern

- enable webhook from workflow integration settings
- send `variables` payloads as JSON body
- use file upload API first when passing file variables
- monitor run history for runtime validation

## Source References

- [OpenAPI Guide](https://github.com/refly-ai/refly/blob/main/docs/en/guide/api/openapi.md)
- [Webhook Guide](https://github.com/refly-ai/refly/blob/main/docs/en/guide/api/webhook.md)
- [README: API Integration Use Case](https://github.com/refly-ai/refly/blob/main/README.md#use-case-1-api-integration)

## Summary

You now have a production-style pattern for calling and monitoring Refly workflows programmatically.

Next: [Chapter 5: Refly CLI and Claude Code Skill Export](05-refly-cli-and-claude-code-skill-export.md)
