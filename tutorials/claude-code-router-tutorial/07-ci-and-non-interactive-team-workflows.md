---
layout: default
title: "Chapter 7: CI and Non-Interactive Team Workflows"
nav_order: 7
parent: Claude Code Router Tutorial
---

# Chapter 7: CI and Non-Interactive Team Workflows

This chapter focuses on reliable CCR execution in automation environments.

## Learning Goals

- configure non-interactive mode correctly for CI jobs
- integrate CCR into GitHub Actions workflows
- avoid stdin-related hangs in automation contexts
- align environment-variable and secret handling across teams

## Automation Checklist

- enable `NON_INTERACTIVE_MODE` where appropriate
- ensure service startup and readiness checks in pipeline
- inject provider secrets securely via CI settings
- monitor fallback and transformer behavior in logs

## Source References

- [README: GitHub Actions](https://github.com/musistudio/claude-code-router/blob/main/README.md#-github-actions)
- [README: Non-Interactive Mode](https://github.com/musistudio/claude-code-router/blob/main/README.md#2-configuration)
- [README: Activate Command](https://github.com/musistudio/claude-code-router/blob/main/README.md#7-activate-command-environment-variables-setup)

## Summary

You now have patterns for stable CCR usage in CI and shared team workflows.

Next: [Chapter 8: Troubleshooting, Security, and Maintenance](08-troubleshooting-security-and-maintenance.md)
