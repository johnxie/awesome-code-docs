---
layout: default
title: "Chapter 7: ACP and Editor Integrations"
nav_order: 7
parent: Mistral Vibe Tutorial
---

# Chapter 7: ACP and Editor Integrations

Vibe includes ACP support so editor clients can run agent workflows through standardized protocol interfaces.

## Integration Path

- use `vibe-acp` as ACP server command
- configure supported editors (Zed, JetBrains, Neovim plugins)
- keep auth/config setup consistent between CLI and ACP sessions

## Source References

- [ACP setup documentation](https://github.com/mistralai/mistral-vibe/blob/main/docs/acp-setup.md)
- [ACP entrypoint implementation](https://github.com/mistralai/mistral-vibe/blob/main/vibe/acp/entrypoint.py)

## Summary

You now have a clear model for connecting Vibe to ACP-capable editor environments.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
