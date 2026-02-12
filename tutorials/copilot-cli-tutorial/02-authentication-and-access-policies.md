---
layout: default
title: "Chapter 2: Authentication and Access Policies"
nav_order: 2
parent: GitHub Copilot CLI Tutorial
---

# Chapter 2: Authentication and Access Policies

Copilot CLI access depends on both local authentication and organization-level Copilot policy settings.

## Authentication Options

| Method | Notes |
|:-------|:------|
| `/login` interactive flow | easiest for most users |
| PAT via `GH_TOKEN` / `GITHUB_TOKEN` | requires Copilot Requests permission |

## Policy Constraints

- Copilot subscription is required.
- Organization/enterprise policy can disable Copilot CLI even when user is licensed.
- Enterprise rollout needs policy verification before onboarding teams.

## Source References

- [Copilot CLI README: prerequisites and auth](https://github.com/github/copilot-cli/blob/main/README.md)
- [GitHub Copilot plans](https://github.com/features/copilot/plans)

## Summary

You now know how to secure Copilot CLI access and avoid common policy blockers.

Next: [Chapter 3: Interactive Workflow and Approval Model](03-interactive-workflow-and-approval-model.md)
