---
layout: default
title: "Chapter 7: Evaluation and Guardrails"
nav_order: 7
parent: Claude Quickstarts Tutorial
---

# Chapter 7: Evaluation and Guardrails

This chapter covers quality evaluation and runtime guardrails for Claude quickstart applications.

## Evaluation Framework

- build task-specific eval sets from real production prompts
- define pass/fail rubrics for factuality, safety, and completeness
- track score deltas for every prompt or workflow change

## Guardrail Layers

- input filters for malformed or abusive payloads
- output checks for policy, PII, and unsafe actions
- tool-call validation with strict schemas

## Release Gating

- block deployments on significant eval regressions
- run canary traffic before full rollout
- capture rollback criteria upfront

## Summary

You can now integrate measurable quality checks with safety controls.

Next: [Chapter 8: Enterprise Operations](08-enterprise-operations.md)
