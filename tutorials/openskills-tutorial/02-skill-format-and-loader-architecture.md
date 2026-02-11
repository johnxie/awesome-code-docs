---
layout: default
title: "Chapter 2: Skill Format and Loader Architecture"
nav_order: 2
parent: OpenSkills Tutorial
---

# Chapter 2: Skill Format and Loader Architecture

OpenSkills uses Claude-style `SKILL.md` and generates an agent-readable skills registry in `AGENTS.md`.

## Architecture Highlights

| Layer | Role |
|:------|:-----|
| skill package | instruction + resources |
| loader | install/read/update lifecycle |
| sync engine | writes `<available_skills>` manifest |

## Summary

You now understand how OpenSkills maps skill files into runtime-usable metadata.

Next: [Chapter 3: Installation Sources and Trust Model](03-installation-sources-and-trust-model.md)
