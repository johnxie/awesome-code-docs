---
layout: default
title: "Chapter 2: LangGraph Architecture and Agent Graphs"
nav_order: 2
parent: Open SWE Tutorial
---

# Chapter 2: LangGraph Architecture and Agent Graphs

This chapter explains the three-graph structure and why it matters.

## Learning Goals

- understand manager/planner/programmer responsibilities
- map graph boundaries to user-visible behavior
- identify extension points for custom forks
- reason about orchestration tradeoffs

## Architecture Pattern

- manager graph coordinates conversations and workflow control
- planner graph generates execution plans for approval
- programmer graph performs code edits and task execution

## Source References

- [Open SWE Docs Intro](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/index.mdx)
- [Open SWE README: Architecture Summary](https://github.com/langchain-ai/open-swe/blob/main/README.md)
- [LangGraph Overview](https://docs.langchain.com/oss/javascript/langgraph/overview)

## Summary

You now understand Open SWE's core orchestration model and where to customize it.

Next: [Chapter 3: Development Environment and Monorepo Setup](03-development-environment-and-monorepo-setup.md)
