---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: AgenticSeek Tutorial
---

# Chapter 1: Getting Started

This chapter gets a clean AgenticSeek baseline running with the official Docker-first flow.

## Learning Goals

- clone and initialize the project safely
- configure baseline environment values in `.env`
- start services and validate backend health
- run first task in web mode and understand expected behavior

## Quick Start Flow

1. Clone and initialize:

```bash
git clone https://github.com/Fosowl/agenticSeek.git
cd agenticSeek
mv .env.example .env
```

2. Update required runtime paths and ports in `.env`:

- set `WORK_DIR` to a real local directory
- keep `SEARXNG_BASE_URL` at `http://searxng:8080` for Docker web mode
- keep API keys empty if running local models only

3. Start full web-mode stack:

```bash
./start_services.sh full
```

4. Wait until backend health checks report ready, then open:

- `http://localhost:3000/`

## First Task Check

Run a simple prompt that requires one tool and one follow-up, for example:

- "Search top three Rust learning resources and save them in my workspace."

You should observe task routing, intermediate tool work, and final answer synthesis.

## Operator Notes

- first Docker run can be slow due image downloads
- use explicit prompts for better routing in early prototype behavior
- avoid broad, ambiguous requests during first validation

## Source References

- [README Prerequisites and Setup](https://github.com/Fosowl/agenticSeek/blob/main/README.md)
- [Start Services Script](https://github.com/Fosowl/agenticSeek/blob/main/start_services.sh)
- [Environment Example](https://github.com/Fosowl/agenticSeek/blob/main/.env.example)

## Summary

You now have a working AgenticSeek baseline in web mode.

Next: [Chapter 2: Architecture and Routing System](02-architecture-and-routing-system.md)
