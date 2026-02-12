---
layout: default
title: "Chapter 8: Contribution Workflow and Versioning Discipline"
nav_order: 8
parent: Compound Engineering Plugin Tutorial
---

# Chapter 8: Contribution Workflow and Versioning Discipline

This chapter explains how contributors evolve the marketplace and compound plugin without destabilizing users.

## Learning Goals

- apply repository versioning and release-discipline rules
- contribute commands/agents/skills with consistent structure
- preserve compatibility across supported provider targets
- document behavior changes for maintainers and users

## Contribution Pattern

1. isolate change scope and affected plugin assets
2. update implementation + docs + examples together
3. run validation checks and integration smoke tests
4. bump versions according to repository rules
5. submit PR with explicit compatibility notes

## Versioning Discipline

- every plugin change should be versioned explicitly
- version changes must be reflected in metadata and changelogs
- cross-provider conversion impacts require extra validation

## Source References

- [Compound Plugin Development Notes](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/CLAUDE.md)
- [Plugin Versioning Requirements](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/solutions/plugin-versioning-requirements.md)
- [Compound Plugin Changelog](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/CHANGELOG.md)

## Summary

You now have an end-to-end approach for contributing to compound engineering plugin systems.

Next steps:

- codify your team's workflow command defaults
- publish compatibility test matrix across target runtimes
- ship one focused contribution with changelog and docs updates
