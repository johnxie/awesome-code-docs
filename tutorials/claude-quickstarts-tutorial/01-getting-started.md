---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Claude Quickstarts Tutorial
---

# Chapter 1: Getting Started

This chapter sets up the quickstarts repository and helps you pick the right project first.

## Clone and Install

```bash
git clone https://github.com/anthropics/anthropic-quickstarts.git
cd anthropic-quickstarts
```

Each quickstart may have its own dependencies. Follow the local README in each project folder.

## Configure Credentials

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

## Choosing Your First Quickstart

- Start with **Customer Support** for straightforward chat workflows.
- Pick **Data Analyst** for structured outputs and visualization.
- Use **Browser/Computer Use** only when automation control is required.

## Success Criteria

- Project boots locally.
- API credentials are loaded securely.
- First request to Claude succeeds.

## Summary

You now have a working local setup and a clear path for selecting a starter quickstart.

Next: [Chapter 2: Customer Support Agents](02-customer-support-agents.md)
