---
layout: default
title: "Chapter 6: Security, Auth, and Operational Constraints"
nav_order: 6
parent: Open SWE Tutorial
---

# Chapter 6: Security, Auth, and Operational Constraints

This chapter surfaces the critical security boundaries in Open SWE deployments.

## Learning Goals

- handle GitHub App credentials and webhook secrets safely
- constrain sandbox and API-key exposure
- manage user access restrictions in shared environments
- document secure operational defaults

## Security Priorities

- protect private keys and webhook secrets
- limit repository permissions to required scopes
- enforce authenticated access boundaries per run
- rotate keys and monitor suspicious webhook activity

## Source References

- [Open SWE Setup: Authentication](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/setup/authentication.mdx)
- [Open SWE Setup: Development](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/setup/development.mdx)
- [Open SWE Security Policy](https://github.com/langchain-ai/open-swe/blob/main/SECURITY.md)

## Summary

You now have a practical security model for operating or auditing Open SWE forks.

Next: [Chapter 7: Fork Maintenance and Migration Strategy](07-fork-maintenance-and-migration-strategy.md)
