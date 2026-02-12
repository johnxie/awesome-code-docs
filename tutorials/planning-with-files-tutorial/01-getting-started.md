---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Planning with Files Tutorial
---

# Chapter 1: Getting Started

This chapter gets the skill installed and running in Claude Code quickly.

## Learning Goals

- install the plugin from marketplace
- run first planning command
- verify files are created in the correct project directory
- confirm baseline workflow is operational

## Quick Install

```bash
/plugin marketplace add OthmanAdi/planning-with-files
/plugin install planning-with-files@planning-with-files
```

## First Command

Use one of:

- `/planning-with-files:plan`
- `/planning-with-files:start`
- `/planning-with-files:status`

## Validation Checklist

- `task_plan.md` created
- `findings.md` created
- `progress.md` created
- hooks/updates behaving as expected

## Source References

- [README Quick Install](https://github.com/OthmanAdi/planning-with-files/blob/master/README.md#quick-install)
- [Quickstart Guide](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/quickstart.md)

## Summary

You now have the baseline workflow installed and active.

Next: [Chapter 2: Core Philosophy and the 3-File Pattern](02-core-philosophy-and-the-3-file-pattern.md)
