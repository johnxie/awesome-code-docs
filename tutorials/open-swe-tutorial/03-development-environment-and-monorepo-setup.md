---
layout: default
title: "Chapter 3: Development Environment and Monorepo Setup"
nav_order: 3
parent: Open SWE Tutorial
---

# Chapter 3: Development Environment and Monorepo Setup

This chapter covers local development setup for teams auditing or maintaining forks.

## Learning Goals

- bootstrap the Yarn/Turbo monorepo correctly
- configure env files and secrets flow
- run web and agent services locally
- avoid setup drift across collaborators

## Setup Highlights

- use Yarn workspaces and Turbo tasks from repo root
- configure both `apps/web` and `apps/open-swe` env files
- establish GitHub App credentials before webhook testing

## Source References

- [Open SWE Development Setup Doc](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/setup/development.mdx)
- [Open SWE AGENTS Rules](https://github.com/langchain-ai/open-swe/blob/main/AGENTS.md)
- [Open SWE Setup Intro](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/setup/intro.mdx)

## Summary

You now have a repeatable local setup baseline for maintenance and experimentation.

Next: [Chapter 4: Usage Patterns: UI and GitHub Workflows](04-usage-patterns-ui-and-github-workflows.md)
