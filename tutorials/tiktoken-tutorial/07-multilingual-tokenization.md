---
layout: default
title: "Chapter 7: Multilingual Tokenization"
nav_order: 7
parent: tiktoken Tutorial
---

# Chapter 7: Multilingual Tokenization

Token-per-character ratios vary widely across scripts and languages, so multilingual systems need language-aware budgeting.

## Why It Matters

A prompt that fits comfortably in one language can exceed context limits in another after localization.

High-variance contributors include:

- script differences (Latin vs CJK vs mixed scripts)
- emoji and symbolic characters
- transliterated names and technical terms

## Benchmarking Pattern

Create a multilingual benchmark set with representative prompts per target locale.

For each locale, track:

- input token count distribution
- output token distribution
- truncation/cutoff rate

## Release Guardrails

| Guardrail | Purpose |
|:----------|:--------|
| locale-specific token budgets | prevent hidden overages |
| pre-release localization token tests | catch oversized prompts early |
| fallback compression strategy | preserve essential context under limits |

## Practical Mitigations

- shorten verbose system text in high-token locales
- move repeated instructions to reusable templates
- summarize long retrieved context before generation

## Summary

You can now design multilingual prompt systems that are budget-aware and resilient across languages.

Next: [Chapter 8: Cost Governance](08-cost-governance.md)
