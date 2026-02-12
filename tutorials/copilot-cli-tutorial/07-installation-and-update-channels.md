---
layout: default
title: "Chapter 7: Installation and Update Channels"
nav_order: 7
parent: GitHub Copilot CLI Tutorial
---

# Chapter 7: Installation and Update Channels

Copilot CLI supports multiple distribution channels suitable for local and enterprise environments.

## Channel Matrix

| Channel | Typical Use |
|:--------|:------------|
| Homebrew | macOS/Linux developer setup |
| WinGet | managed Windows rollout |
| npm | cross-platform package-manager workflows |
| install script | direct binary installation and custom prefix control |

## Update Strategy

- pin version where deterministic behavior matters
- review changelog before team-wide upgrades
- keep preview clients current when testing experimental features

## Source References

- [Copilot CLI README: install options](https://github.com/github/copilot-cli/blob/main/README.md)
- [Install script details](https://github.com/github/copilot-cli/blob/main/install.sh)
- [Copilot CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md)

## Summary

You now have a rollout model for stable and controlled Copilot CLI upgrades.

Next: [Chapter 8: Production Governance and Team Rollout](08-production-governance-and-team-rollout.md)
