---
layout: default
title: "Chapter 6: Auth System"
nav_order: 6
has_children: false
parent: "NocoDB Database Platform"
---

# Chapter 6: Auth System

Authentication and authorization enforce tenant boundaries and protect data operations.

## Auth Layer Capabilities

- identity/session or token lifecycle management
- role- and workspace-scoped permission checks
- API-level access enforcement for tables/views/actions
- audit event generation for privileged changes

## Authorization Model

A robust NocoDB deployment typically applies checks at multiple layers:

1. API boundary (request identity and role)
2. domain service layer (action permissions)
3. data layer (row/table/workspace constraints)

## Production Controls

| Control | Purpose |
|:--------|:--------|
| short-lived access tokens | reduce blast radius of credential leakage |
| refresh-token rotation | mitigate token replay risk |
| least-privilege role design | minimize unnecessary access |
| immutable audit logs | support incident response and compliance |

## Common Failure Modes

- role drift due to ad hoc permission grants
- missing checks on non-UI API paths
- unclear ownership of privileged operations

## Summary

You now understand the access-control architecture needed for secure multi-user NocoDB operations.

Next: [Chapter 7: Vue Components](07-vue-components.md)
