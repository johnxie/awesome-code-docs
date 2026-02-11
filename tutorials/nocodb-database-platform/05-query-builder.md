---
layout: default
title: "Chapter 5: Query Builder"
nav_order: 5
has_children: false
parent: "NocoDB Database Platform"
---

# Chapter 5: Query Builder

NocoDB's query builder translates UI filters and API params into SQL safely.

## Builder Responsibilities

- map logical filter expressions to SQL predicates
- preserve DB-specific dialect compatibility
- support sorting, pagination, and joins
- enforce column/type validation before execution

## Safety Rules

- parameterized queries only
- allowlisted operators per type
- bounded pagination defaults

## Summary

You can now reason about NocoDB query planning between spreadsheet UX and SQL backends.

Next: [Chapter 6: Auth System](06-auth-system.md)
