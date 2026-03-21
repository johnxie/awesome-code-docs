---
layout: default
title: "Chapter 2: Architecture and Runtime Components"
nav_order: 2
parent: Tabby Tutorial
---


# Chapter 2: Architecture and Runtime Components

Welcome to **Chapter 2: Architecture and Runtime Components**. In this part of **Tabby Tutorial: Self-Hosted AI Coding Assistant Architecture and Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Tabby is more than a single completion endpoint. It is a layered runtime that combines server services, context processing, and editor-facing agent bridges.

## Learning Goals

- map major runtime components and boundaries
- understand request flow from editor to model backend
- identify where to place custom integrations and controls

## Core Component Map

| Component | Responsibility |
|:----------|:---------------|
| Tabby server | serves completion/chat APIs and admin web UI |
| `tabby-agent` | LSP bridge between editors and Tabby APIs |
| editor extension | user interaction layer for completion/chat |
| model backends | completion/chat/embedding inference providers |
| indexing subsystem | builds repository and document context |

## Runtime Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Ext as Editor Extension
    participant Agent as tabby-agent
    participant Srv as Tabby Server
    participant Model as Model Backend

    Dev->>Ext: trigger completion/chat
    Ext->>Agent: send LSP request
    Agent->>Srv: call Tabby API
    Srv->>Model: inference request with context
    Model-->>Srv: generated output
    Srv-->>Agent: completion/chat payload
    Agent-->>Ext: LSP response
    Ext-->>Dev: inline result
```

## Repository Structure Orientation

| Path | Why You Care |
|:-----|:-------------|
| `clients/` | extension and agent-side integration patterns |
| `crates/` | core server/runtime internals implemented in Rust |
| `website/docs/` | operational and configuration guidance |
| `ee/` | enterprise-oriented modules and integrations |

## Design Implications

- API and LSP boundaries let teams update editor adapters independently.
- Model provider abstraction enables mixed local and remote deployment strategy.
- Context indexing is a first-class system, not an optional add-on.

## Source References

- [Tabby Repository Layout](https://github.com/TabbyML/tabby)
- [Welcome Docs](https://tabby.tabbyml.com/docs/welcome/)
- [tabby-agent README](https://github.com/TabbyML/tabby/blob/main/clients/tabby-agent/README.md)

## Summary

You now have a structural map for where behavior lives and how requests move across Tabby.

Next: [Chapter 3: Model Serving and Completion Pipeline](03-model-serving-and-completion-pipeline.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `rules/use-schema-result.yml`

The `severity` interface in [`rules/use-schema-result.yml`](https://github.com/TabbyML/tabby/blob/HEAD/rules/use-schema-result.yml) handles a key part of this chapter's functionality:

```yml
id: use-schema-result
message: Use schema::Result as API interface
severity: error
language: rust
files:
- ./ee/tabby-schema/src/**
ignores:
- ./ee/tabby-schema/src/lib.rs
- ./ee/tabby-schema/src/dao.rs
rule:
  any:
    - pattern: anyhow
      not:
        inside:
          kind: enum_variant
          stopBy: end
    - pattern: FieldResult
```

This interface is important because it defines how Tabby Tutorial: Self-Hosted AI Coding Assistant Architecture and Operations implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[severity]
```
