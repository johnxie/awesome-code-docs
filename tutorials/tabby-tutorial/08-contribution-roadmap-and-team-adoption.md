---
layout: default
title: "Chapter 8: Contribution, Roadmap, and Team Adoption"
nav_order: 8
parent: Tabby Tutorial
---


# Chapter 8: Contribution, Roadmap, and Team Adoption

Welcome to **Chapter 8: Contribution, Roadmap, and Team Adoption**. In this part of **Tabby Tutorial: Self-Hosted AI Coding Assistant Architecture and Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter closes the track with contribution mechanics and rollout strategy for engineering organizations.

## Learning Goals

- map a phased adoption plan for teams
- contribute changes to Tabby with minimal friction
- align roadmap signals with your internal platform needs

## Team Rollout Model

| Phase | Outcome |
|:------|:--------|
| pilot | small engineering group validates quality and workflow fit |
| expansion | additional teams onboard with shared policy templates |
| platformization | Tabby becomes part of standard developer environment |

## Contribution Workflow

1. clone repository with submodules when needed
2. follow `CONTRIBUTING.md` setup guidance
3. build and run tests for touched modules
4. submit focused PRs with clear behavior change notes

## Governance Checklist

- define ownership for runtime config and upgrades
- standardize model/provider policies across teams
- maintain internal runbooks for incidents and user onboarding

## Source References

- [Contributing Guide](https://github.com/TabbyML/tabby/blob/main/CONTRIBUTING.md)
- [Roadmap](https://tabby.tabbyml.com/docs/roadmap)
- [Tabby Repository](https://github.com/TabbyML/tabby)

## Summary

You now have a full lifecycle mental model for adopting, operating, and extending Tabby as an internal coding assistant platform.

Next: pick a related implementation track such as [Continue](../continue-tutorial/) or [OpenCode](../opencode-tutorial/).

## Source Code Walkthrough

### `Cargo.toml`

The `Cargo` module in [`Cargo.toml`](https://github.com/TabbyML/tabby/blob/HEAD/Cargo.toml) handles a key part of this chapter's functionality:

```toml
[workspace]
resolver = "1"
members = [
    "crates/tabby",
    "crates/tabby-common",
    "crates/tabby-download",
    "crates/tabby-git",
    "crates/tabby-inference",
    "crates/tabby-index",
    "crates/tabby-crawler",

    "crates/aim-downloader",
    "crates/http-api-bindings",
    "crates/llama-cpp-server",
    "crates/ollama-api-bindings",
    "crates/tabby-index-cli",
    "crates/hash-ids",
    "crates/sqlx-migrate-validate",

    "ee/tabby-webserver",
    "ee/tabby-db",
    "ee/tabby-db-macros",
    "ee/tabby-schema",
]

[workspace.package]
version = "0.33.0-dev.0"
edition = "2021"
authors = ["TabbyML Team"]
homepage = "https://github.com/TabbyML/tabby"

[workspace.dependencies]
cached = "0.49.3"
lazy_static = "1.4.0"
serde = { version = "1.0", features = ["derive"] }
```

This module is important because it defines how Tabby Tutorial: Self-Hosted AI Coding Assistant Architecture and Operations implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[Cargo]
```
