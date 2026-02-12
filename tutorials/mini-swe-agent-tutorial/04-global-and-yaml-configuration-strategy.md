---
layout: default
title: "Chapter 4: Global and YAML Configuration Strategy"
nav_order: 4
parent: Mini-SWE-Agent Tutorial
---

# Chapter 4: Global and YAML Configuration Strategy

This chapter maps configuration layers for reproducible behavior.

## Learning Goals

- separate global environment settings from run config
- structure YAML files for agent/environment/model/run
- avoid config drift across contributors
- keep templates and parsing rules maintainable

## Config Guidance

- use global config for credentials/defaults
- use YAML for run-specific behavior and templates
- version config presets for reproducible evaluations

## Source References

- [Global Configuration](https://mini-swe-agent.com/latest/advanced/global_configuration/)
- [YAML Configuration](https://mini-swe-agent.com/latest/advanced/yaml_configuration/)
- [Usage Config Docs](https://mini-swe-agent.com/latest/usage/config/)

## Summary

You now have a disciplined configuration strategy for mini-swe-agent.

Next: [Chapter 5: Environments, Sandboxing, and Deployment](05-environments-sandboxing-and-deployment.md)
