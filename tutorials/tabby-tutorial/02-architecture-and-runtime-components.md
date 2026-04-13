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

## Source Code Walkthrough

Use the following upstream sources to verify architecture and runtime component details while reading this chapter:

- [`Cargo.toml`](https://github.com/TabbyML/tabby/blob/HEAD/Cargo.toml) — the Rust workspace manifest that lists all crates composing the Tabby runtime: `tabby`, `tabby-common`, `tabby-inference`, `tabby-index`, `tabby-crawler`, and the enterprise `ee/` components.
- [`crates/tabby-inference/src/lib.rs`](https://github.com/TabbyML/tabby/blob/HEAD/crates/tabby-inference/src/lib.rs) — the inference abstraction layer that defines the `TextGenerationStream` trait implemented by each model backend (llama.cpp, GGML, HTTP API).

Suggested trace strategy:
- read `Cargo.toml` to map the crate dependency graph and identify which crates handle serving, inference, and indexing
- trace `tabby-inference/src/lib.rs` to understand the trait abstraction that decouples the API server from specific model backends
- review `crates/tabby-common/` for shared data types (completion request/response, configuration structs) used across crates

## How These Components Connect

```mermaid
flowchart LR
    A[HTTP API request] --> B[tabby crate: request routing]
    B --> C[tabby-inference: TextGenerationStream trait]
    C --> D[Backend: llama.cpp or GGML or HTTP model]
    D --> E[Completion tokens streamed back]
```