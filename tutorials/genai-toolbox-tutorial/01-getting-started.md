---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: GenAI Toolbox Tutorial
---

# Chapter 1: Getting Started

This chapter gets a local Toolbox instance running against a real database quickly.

## Learning Goals

- run Toolbox with a minimal `tools.yaml`
- connect a local database and verify first tool execution
- understand quickstart differences between MCP and SDK workflows
- establish a repeatable local baseline before extending scope

## Fast Start Loop

1. prepare database prerequisites (for example PostgreSQL)
2. define `sources` and one tool in `tools.yaml`
3. run Toolbox (`npx @toolbox-sdk/server --tools-file tools.yaml` or local binary)
4. connect from an SDK or MCP client and execute the tool
5. capture working config as your baseline template

## Source References

- [README Quickstart](https://github.com/googleapis/genai-toolbox/blob/main/README.md)
- [Python Local Quickstart](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/getting-started/local_quickstart.md)
- [Toolbox Server README](https://github.com/googleapis/genai-toolbox/blob/main/docs/TOOLBOX_README.md)

## Summary

You now have a validated local loop for running and invoking Toolbox tools.

Next: [Chapter 2: Architecture and Control Plane](02-architecture-and-control-plane.md)
