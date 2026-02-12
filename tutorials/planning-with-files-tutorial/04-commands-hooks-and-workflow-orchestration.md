---
layout: default
title: "Chapter 4: Commands, Hooks, and Workflow Orchestration"
nav_order: 4
parent: Planning with Files Tutorial
---

# Chapter 4: Commands, Hooks, and Workflow Orchestration

This chapter explains how command entrypoints and hooks enforce planning discipline.

## Learning Goals

- use commands for consistent task entry and status checks
- understand hook responsibilities during execution lifecycle
- apply the 2-action rule and completion checks correctly
- reduce skipped-update and missed-error behavior

## Command Surface

- `plan`: initialize or continue planning session
- `status`: quick planning progress snapshot
- `start`: original entrypoint alias

## Hook Functions

- remind on stale planning updates
- re-read plan before major actions
- verify completion before stop

## Source References

- [Commands Directory](https://github.com/OthmanAdi/planning-with-files/tree/master/commands)
- [Workflow Guide](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/workflow.md)
- [README Usage Section](https://github.com/OthmanAdi/planning-with-files/blob/master/README.md#usage)

## Summary

You now know how orchestration components enforce workflow consistency.

Next: [Chapter 5: Templates, Scripts, and Session Recovery](05-templates-scripts-and-session-recovery.md)
