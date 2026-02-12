---
layout: default
title: "Chapter 4: Model Providers and Runtime Strategy"
nav_order: 4
parent: Strands Agents Tutorial
---

# Chapter 4: Model Providers and Runtime Strategy

This chapter explains provider selection and runtime tuning decisions.

## Learning Goals

- choose model providers based on constraints
- configure parameters for quality/cost/latency tradeoffs
- use provider abstractions cleanly
- avoid lock-in through adapter-friendly architecture

## Provider Strategy

- start with one provider for baseline reliability
- use explicit model IDs and params in code
- benchmark task classes before multi-provider expansion

## Source References

- [Strands Model Provider Concepts](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/)
- [Strands README: Multiple Model Providers](https://github.com/strands-agents/sdk-python#multiple-model-providers)
- [Strands Custom Provider Docs](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/model-providers/custom_model_provider/)

## Summary

You can now make provider decisions that align with product and operations goals.

Next: [Chapter 5: Hooks, State, and Reliability Controls](05-hooks-state-and-reliability-controls.md)
