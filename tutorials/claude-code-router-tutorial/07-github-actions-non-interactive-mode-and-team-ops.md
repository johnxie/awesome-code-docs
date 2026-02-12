---
layout: default
title: "Chapter 7: GitHub Actions, Non-Interactive Mode, and Team Ops"
nav_order: 7
parent: Claude Code Router Tutorial
---

# Chapter 7: GitHub Actions, Non-Interactive Mode, and Team Ops

This chapter explains how to run CCR in automation contexts and shared team environments.

## Learning Goals

- configure `NON_INTERACTIVE_MODE` for CI reliability
- integrate CCR with GitHub Actions and Claude Code Actions
- avoid stdin and terminal assumptions in automation runs
- standardize environment variables across team tooling

## Automation Checklist

- set `NON_INTERACTIVE_MODE: true` in CI config
- ensure router service startup before action execution
- pass provider secrets through secure CI secret stores
- verify logs for failed route/fallback transitions

## Source References

- [README: GitHub Actions](https://github.com/musistudio/claude-code-router/blob/main/README.md#-github-actions)
- [README: Non-Interactive Mode](https://github.com/musistudio/claude-code-router/blob/main/README.md#2-configuration)
- [README: Activate Command](https://github.com/musistudio/claude-code-router/blob/main/README.md#7-activate-command-environment-variables-setup)

## Summary

You now have patterns for running CCR in automated and team-scale workflows.

Next: [Chapter 8: Troubleshooting, Security, and Contribution Workflow](08-troubleshooting-security-and-contribution-workflow.md)
