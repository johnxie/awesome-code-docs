---
layout: default
title: "Chapter 6: Auth System"
nav_order: 6
has_children: false
parent: "NocoDB Database Platform"
---

# Chapter 6: Auth System

Authentication and authorization enforce tenant boundaries and role-based access.

## Core Capabilities

- identity management and session/token issuance
- role-based permissions for tables/views/actions
- workspace-level access control and audit logs

## Production Practices

- short-lived tokens + refresh flows
- permission checks at API boundary and data layer
- immutable audit events for privileged actions

## Summary

You now understand NocoDB's access-control design and operational safeguards.

Next: [Chapter 7: Vue Components](07-vue-components.md)
