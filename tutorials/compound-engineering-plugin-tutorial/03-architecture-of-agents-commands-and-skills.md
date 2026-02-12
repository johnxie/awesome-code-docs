---
layout: default
title: "Chapter 3: Architecture of Agents, Commands, and Skills"
nav_order: 3
parent: Compound Engineering Plugin Tutorial
---

# Chapter 3: Architecture of Agents, Commands, and Skills

This chapter maps the plugin's capability graph across agents, commands, and skills.

## Learning Goals

- understand capability categories and their purposes
- map commands to underlying specialist agents and skills
- design workflow routing decisions with less trial-and-error
- identify where to add customizations safely

## Capability Topology

The plugin organizes assets into:

- review agents
- research agents
- design agents
- workflow agents
- command suites
- skill packs across architecture, tooling, orchestration, and automation

## Practical Mapping Pattern

- use workflow commands for default orchestration
- invoke targeted commands for specialized tasks
- rely on skills for repeatable domain strategy injection

## Source References

- [Compound Plugin Components](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/README.md#components)
- [Agents Catalog](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/agents)
- [Commands Catalog](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/commands)
- [Skills Catalog](https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering/skills)

## Summary

You now have a clear architecture map for plugin capability selection.

Next: [Chapter 4: Multi-Provider Conversion and Config Sync](04-multi-provider-conversion-and-config-sync.md)
