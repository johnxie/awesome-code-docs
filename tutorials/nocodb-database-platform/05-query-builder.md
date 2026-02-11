---
layout: default
title: "Chapter 5: Query Builder"
nav_order: 5
has_children: false
parent: "NocoDB Database Platform"
---

# Chapter 5: Query Builder

NocoDB's query builder is the translation layer between spreadsheet-style UI operations and SQL execution.

## Core Responsibilities

- convert filter groups into SQL predicates
- map sort and pagination controls to stable query clauses
- resolve relation-aware joins from UI context
- validate column/operator/type compatibility before execution

## Translation Pipeline

1. parse UI query state into intermediate expression tree
2. normalize operators by data type
3. generate parameterized SQL with bound values
4. execute with workspace/table-level access checks

## Safety and Correctness Rules

| Rule | Why It Matters |
|:-----|:---------------|
| parameterized queries only | prevents injection attacks |
| operator allowlists by type | avoids invalid or unsafe expressions |
| bounded pagination defaults | protects database from unbounded scans |
| deterministic sort fallback | stable results across pages |

## Performance Considerations

- index-aware predicate ordering
- selective projection to avoid overfetching
- optional query plan inspection for expensive views

## Summary

You can now reason about how NocoDB maps end-user filters into safe, efficient SQL.

Next: [Chapter 6: Auth System](06-auth-system.md)
