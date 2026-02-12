---
layout: default
title: "Chapter 3: Swarm Coordination and Consensus Patterns"
nav_order: 3
parent: Claude Flow Tutorial
---

# Chapter 3: Swarm Coordination and Consensus Patterns

This chapter focuses on multi-agent topology, role assignment, and coordination protocols.

## Learning Goals

- choose topology patterns based on scale and latency tradeoffs
- route tasks by domain and capability boundaries
- evaluate consensus mode choices for risk tolerance
- avoid over-coordination overhead on simple workloads

## Coordination Rule of Thumb

Use hierarchical or centralized patterns for clearer control paths, switch to hybrid when scale or domain parallelism increases, and reserve heavier consensus settings for high-risk decisions.

## Source References

- [@claude-flow/swarm](https://github.com/ruvnet/claude-flow/blob/main/v3/@claude-flow/swarm/README.md)
- [README](https://github.com/ruvnet/claude-flow/blob/main/README.md)
- [V3 README](https://github.com/ruvnet/claude-flow/blob/main/v3/README.md)

## Summary

You can now design swarm coordination with clearer topology and consensus tradeoffs.

Next: [Chapter 4: Memory, Learning, and Intelligence Systems](04-memory-learning-and-intelligence-systems.md)
