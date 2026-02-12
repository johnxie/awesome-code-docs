---
layout: default
title: "Chapter 6: Versioning, Governance, and Moderation Lifecycle"
nav_order: 6
parent: MCP Registry Tutorial
---

# Chapter 6: Versioning, Governance, and Moderation Lifecycle

Registry metadata is designed to be append-oriented and version-immutable, with lifecycle signaling through status and moderation operations.

## Learning Goals

- apply versioning strategy that avoids accidental "latest" regressions
- distinguish immutable metadata from mutable status fields
- understand moderation and abuse-handling implications for consumers
- plan governance policies for your own subregistry or internal mirror

## Versioning Guidance

| Practice | Why |
|:---------|:----|
| semantic versioning where possible | stable sort + predictable latest behavior |
| avoid version ranges | explicitly prohibited in official validation |
| align server/package versions for local servers | reduces operator confusion |
| use prerelease tags for metadata-only publishes | keeps artifact version semantics clearer |

## Governance Detail

Consumers should treat `deleted` as a strong trust signal and remove or quarantine those entries from user-facing catalogs.

## Source References

- [Versioning Guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/versioning.mdx)
- [FAQ](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/faq.mdx)
- [Official Registry Requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)

## Summary

You now have lifecycle rules for safer metadata governance.

Next: [Chapter 7: Admin Operations, Deployment, and Observability](07-admin-operations-deployment-and-observability.md)
