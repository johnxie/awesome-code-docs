---
layout: default
title: "Chapter 4: Terminal and Runtime Tools"
nav_order: 4
parent: Cline Tutorial
---

# Chapter 4: Terminal and Runtime Tools

Terminal execution lets Cline move beyond static edits into full engineering loops.

## Command Execution Capabilities

- run build/test/lint commands
- install dependencies
- inspect runtime logs
- react to failing output with follow-up edits

## Long-Running Command Pattern

For development servers or watchers, use proceed-while-running patterns so Cline can continue work while monitoring output.

## Safety Controls

- keep explicit approval for commands
- avoid broad destructive shell operations
- use allowlists for high-risk environments

## Reliability Practices

- pin canonical test command per repo
- keep command outputs in task trace
- fail fast on repeated non-deterministic command errors

## Summary

You can now use Cline’s terminal toolchain for iterative build-fix-validate workflows.

Next: [Chapter 5: Browser Automation](05-browser-automation.md)
