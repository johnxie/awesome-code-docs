---
layout: default
title: "Chapter 7: Troubleshooting, Permissions, and Security"
nav_order: 7
parent: MCP Chrome Tutorial
---

# Chapter 7: Troubleshooting, Permissions, and Security

Most MCP Chrome failures are installation or permission issues. This chapter turns those into a deterministic runbook.

## Learning Goals

- diagnose native host and registration failures quickly
- resolve platform-specific permission issues safely
- apply practical security boundaries in browser automation

## Common Failure Classes

| Class | Example |
|:------|:--------|
| registration failure | native host manifest missing or wrong path |
| permission error | execute permissions missing for bridge scripts |
| client transport mismatch | streamable HTTP config in stdio-only client |
| extension connectivity | native messaging host not detected |

## Security Practices

- treat browser automation tools as privileged operations
- keep extension permissions minimal and audited
- require human oversight for destructive or account-sensitive actions

## Source References

- [Troubleshooting](https://github.com/hangwin/mcp-chrome/blob/master/docs/TROUBLESHOOTING.md)
- [Native Install Guide](https://github.com/hangwin/mcp-chrome/blob/master/app/native-server/install.md)
- [Issue Template/Guide](https://github.com/hangwin/mcp-chrome/blob/master/docs/ISSUE.md)

## Summary

You now have a concrete troubleshooting and safety baseline for MCP Chrome operations.

Next: [Chapter 8: Contribution, Release, and Runtime Operations](08-contribution-release-and-runtime-operations.md)
