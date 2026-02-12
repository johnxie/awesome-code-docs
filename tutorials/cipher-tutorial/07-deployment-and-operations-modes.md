---
layout: default
title: "Chapter 7: Deployment and Operations Modes"
nav_order: 7
parent: Cipher Tutorial
---

# Chapter 7: Deployment and Operations Modes

Cipher can run locally, in containers, or as service components depending on deployment needs.

## Deployment Patterns

- local npm install for developer workflows
- Docker/compose for shared service setups
- API + Web UI for team-facing memory services

## Operations Guidance

- keep environment-variable secrets externalized
- monitor memory store health and API endpoints
- validate transport/client compatibility during upgrades

## Source References

- [Cipher README deployment sections](https://github.com/campfirein/cipher/blob/main/README.md)
- [Nginx/proxy deployment docs](https://github.com/campfirein/cipher/blob/main/docs/deployment-nginx-proxy.md)

## Summary

You now have deployment and operations patterns for running Cipher in developer and team environments.

Next: [Chapter 8: Security and Team Governance](08-security-and-team-governance.md)
