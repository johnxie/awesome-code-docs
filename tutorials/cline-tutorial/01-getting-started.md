---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Cline Tutorial
---

# Chapter 1: Getting Started

This chapter sets up Cline in VS Code and validates the core agent loop.

## Install Path

1. install Cline from the VS Code marketplace
2. configure provider/API credentials in extension settings
3. open a test repository
4. issue a small bounded task

## First Task Pattern

Use a low-risk task for first validation:

- summarize project structure
- add a tiny utility function
- run one existing test command

This tests analysis, edit, and execution capabilities together.

## Safety Defaults

Cline is designed around explicit user approvals for actions such as terminal commands and file edits. Keep this enabled while calibrating prompts and workflows.

## Baseline Checklist

- extension can read relevant project files
- proposed file changes appear as reviewable diffs
- terminal command outputs are captured correctly
- task can complete with deterministic summary

## Summary

You now have a working Cline setup and a safe baseline for deeper agent workflows.

Next: [Chapter 2: Agent Workflow](02-agent-workflow.md)
