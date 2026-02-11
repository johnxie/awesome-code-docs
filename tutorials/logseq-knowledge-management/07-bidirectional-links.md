---
layout: default
title: "Chapter 7: Bi-Directional Links"
nav_order: 7
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 7: Bi-Directional Links

Bi-directional links transform notes from isolated documents into a navigable knowledge graph.

## Link Lifecycle

1. user creates inline reference (for example `[[Page]]`)
2. parser detects outbound relation
3. index updates backlinks for target entity/page
4. search and graph views expose both directions

## Why Bi-Directional Links Matter

- discovery of related ideas without manual cross-indexing
- emergent structure from everyday note-taking
- contextual navigation through backlinks and linked references

## Consistency Concerns

- renamed pages must retain link integrity
- deleted targets need clear broken-link handling
- partial file edits should not produce stale backlink indexes

## Scaling Considerations

- backlink queries should be incremental and cached
- graph updates should avoid full reindex on small edits
- visualization should limit edge rendering for large graphs

## Summary

You now understand how Logseq derives connected knowledge structure directly from inline references.

Next: [Chapter 8: Graph Visualization](08-graph-visualization.md)
