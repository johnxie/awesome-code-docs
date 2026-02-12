---
layout: default
title: "Chapter 7: Troubleshooting and Reliability Playbook"
nav_order: 7
parent: AgenticSeek Tutorial
---

# Chapter 7: Troubleshooting and Reliability Playbook

This chapter covers the failure modes you will hit most often and how to recover quickly.

## Learning Goals

- diagnose ChromeDriver compatibility failures
- fix provider connection adapter errors
- resolve SearxNG endpoint misconfiguration
- build a repeatable incident triage routine

## High-Frequency Issues

### ChromeDriver Version Mismatch

Symptoms:

- `SessionNotCreatedException`
- browser startup failures in automation tasks

First actions:

- verify local browser version
- install matching ChromeDriver major version
- ensure executable permissions and correct location

### Provider Connection Adapter Errors

Symptoms:

- errors like "No connection adapters were found"

First actions:

- confirm `provider_server_address` includes protocol (`http://`)
- verify model server endpoint and port reachability

### Missing SearxNG Base URL

Symptoms:

- `SearxNG base URL must be provided` runtime error

First actions:

- set `SEARXNG_BASE_URL` based on mode
- use `http://searxng:8080` in Docker web mode
- use `http://localhost:8080` in host CLI mode

## Reliability Habit Loop

- reproduce with smallest possible prompt
- isolate to config, provider, browser, or tool layer
- capture logs and final config deltas
- only then widen back to full task scope

## Source References

- [README Troubleshooting](https://github.com/Fosowl/agenticSeek/blob/main/README.md#troubleshooting)
- [README ChromeDriver Issues](https://github.com/Fosowl/agenticSeek/blob/main/README.md#chromedriver-issues)
- [README FAQ](https://github.com/Fosowl/agenticSeek/blob/main/README.md#faq)

## Summary

You now have a practical incident-response playbook for AgenticSeek operations.

Next: [Chapter 8: Contribution Workflow and Project Governance](08-contribution-workflow-and-project-governance.md)
