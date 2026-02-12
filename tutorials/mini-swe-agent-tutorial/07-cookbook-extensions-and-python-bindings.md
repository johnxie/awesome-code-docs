---
layout: default
title: "Chapter 7: Cookbook Extensions and Python Bindings"
nav_order: 7
parent: Mini-SWE-Agent Tutorial
---

# Chapter 7: Cookbook Extensions and Python Bindings

This chapter shows how to extend behavior without bloating the core.

## Learning Goals

- use cookbook patterns for custom components
- extend agents/environments/models with minimal coupling
- keep custom scripts maintainable
- preserve simplicity during extension work

## Extension Strategy

- prefer composable component overrides
- avoid adding broad knobs to core components
- keep custom logic in focused run scripts or extra modules

## Source References

- [Cookbook](https://mini-swe-agent.com/latest/advanced/cookbook/)
- [Python Bindings Usage](https://mini-swe-agent.com/latest/usage/python_bindings/)
- [Project Source Tree](https://github.com/SWE-agent/mini-swe-agent/tree/main/src/minisweagent)

## Summary

You now have a path to custom behavior while preserving the minimal architecture.

Next: [Chapter 8: Contribution Workflow and Governance](08-contribution-workflow-and-governance.md)
