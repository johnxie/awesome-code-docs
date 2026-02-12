---
layout: default
title: "Chapter 2: V3 Architecture and ADRs"
nav_order: 2
parent: Claude Flow Tutorial
---

# Chapter 2: V3 Architecture and ADRs

This chapter explains the V3 module split and ADR-driven architecture decisions.

## Learning Goals

- map core V3 modules to their responsibilities
- understand ADR intent behind architecture choices
- identify where V2 assumptions no longer apply cleanly
- prioritize modules based on your adoption stage

## Architecture Reading Order

Start with the V3 README for module topology, then review the ADR index to understand decision intent, and finally map required modules (swarm, mcp, memory, security, testing) to your own workload constraints.

## Source References

- [V3 README](https://github.com/ruvnet/claude-flow/blob/main/v3/README.md)
- [V3 ADR Index](https://github.com/ruvnet/claude-flow/blob/main/v3/docs/adr/README.md)
- [V3 Implementation Docs](https://github.com/ruvnet/claude-flow/blob/main/v3/implementation/README.md)

## Summary

You now have a grounded model of how V3 is structured and how ADRs shape implementation priorities.

Next: [Chapter 3: Swarm Coordination and Consensus Patterns](03-swarm-coordination-and-consensus-patterns.md)
