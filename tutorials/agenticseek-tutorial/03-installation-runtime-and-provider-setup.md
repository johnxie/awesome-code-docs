---
layout: default
title: "Chapter 3: Installation, Runtime, and Provider Setup"
nav_order: 3
parent: AgenticSeek Tutorial
---


# Chapter 3: Installation, Runtime, and Provider Setup

Welcome to **Chapter 3: Installation, Runtime, and Provider Setup**. In this part of **AgenticSeek Tutorial: Local-First Autonomous Agent Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter makes provider and runtime settings reproducible so setup drift does not break sessions.

## Learning Goals

- configure `config.ini` with valid provider/server values
- choose local vs API mode intentionally
- align `.env` and `config.ini` settings to operation mode
- validate configuration before full task execution

## Key Configuration Surfaces

- `.env`: infrastructure and secret settings (`SEARXNG_BASE_URL`, keys, workspace path)
- `config.ini`: provider behavior and runtime toggles (`is_local`, `provider_name`, `provider_model`)

## Baseline Local Provider Example

```ini
[MAIN]
is_local = True
provider_name = ollama
provider_model = deepseek-r1:14b
provider_server_address = http://127.0.0.1:11434
agent_name = Friday
recover_last_session = True
save_session = True

[BROWSER]
headless_browser = True
stealth_mode = True
```

## Common Configuration Errors

- missing `http://` in `provider_server_address`
- `provider_name` mismatch (`openai` vs `lm-studio` when running locally)
- invalid `WORK_DIR` path causing file operation failures
- copying commented config examples directly into strict INI parser contexts

## Validation Steps

- confirm provider endpoint is reachable before launching tasks
- verify docker services (`searxng`, `redis`, backend) are healthy
- run a file-write task to confirm workspace permissions

## Source References

- [README Config Section](https://github.com/Fosowl/agenticSeek/blob/main/README.md#config)
- [Default Config File](https://github.com/Fosowl/agenticSeek/blob/main/config.ini)
- [Install Script](https://github.com/Fosowl/agenticSeek/blob/main/install.sh)

## Summary

You now have a repeatable provider/runtime configuration strategy.

Next: [Chapter 4: Docker Web Mode and CLI Operations](04-docker-web-mode-and-cli-operations.md)

## Source Code Walkthrough

### `config.ini` and provider initialization

Installation and provider configuration in AgenticSeek are driven by [`config.ini`](https://github.com/Fosowl/agenticSeek/blob/HEAD/config.ini), which defines the active provider, model paths, and speech settings. The `cli.py` main function reads this file at startup and constructs the appropriate provider instance — making it the central reference for Chapter 3's provider setup guidance.

The [`sources/providers.py`](https://github.com/Fosowl/agenticSeek/blob/HEAD/sources/providers.py) module implements the provider abstraction, showing how local Ollama endpoints, OpenAI-compatible APIs, and remote server connections are initialized from the config file.