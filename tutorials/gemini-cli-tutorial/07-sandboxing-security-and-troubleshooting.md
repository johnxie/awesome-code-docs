---
layout: default
title: "Chapter 7: Sandboxing, Security, and Troubleshooting"
nav_order: 7
parent: Gemini CLI Tutorial
---

# Chapter 7: Sandboxing, Security, and Troubleshooting

This chapter focuses on safe execution and common failure recovery.

## Learning Goals

- enable and validate sandbox modes
- reason about trusted-folder and execution-risk controls
- troubleshoot auth, command, and environment failures
- establish repeatable incident diagnosis loops

## Sandboxing Modes

Gemini CLI supports host and containerized approaches depending on platform constraints.

- macOS Seatbelt for local constrained execution
- Docker/Podman container sandboxing for broader isolation

## Practical Security Controls

- use trusted-folder policies intentionally
- constrain risky operations in shared environments
- prefer read-only validation tasks for first-run integrations

## Troubleshooting Focus Areas

- authentication and login failures
- model/access configuration conflicts
- MCP server connectivity and auth issues
- sandbox setup and runtime environment mismatches

## Source References

- [Sandboxing Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/sandbox.md)
- [Trusted Folders Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/trusted-folders.md)
- [Troubleshooting Guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/troubleshooting.md)
- [Security Policy](https://github.com/google-gemini/gemini-cli/blob/main/SECURITY.md)

## Summary

You now have a reliability and risk-control playbook for Gemini CLI operations.

Next: [Chapter 8: Contribution Workflow and Enterprise Operations](08-contribution-workflow-and-enterprise-operations.md)
