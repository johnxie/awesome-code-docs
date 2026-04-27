---
layout: default
title: Hermes Agent Tutorial
nav_order: 42
has_children: true
format_version: v2
source_repo: https://github.com/nousresearch/hermes-agent
categories: [ai-agents, personal-ai, multi-platform, rl-training]
related_tutorials:
  - openclaw-tutorial
  - mem0-tutorial
  - taskade-tutorial
  - agno-tutorial
last_updated: 2026-04-12
---

# Hermes Agent Tutorial

**NousResearch's self-hosted personal AI agent with persistent memory, autonomous skill creation, 20+ platform gateway, and a closed reinforcement-learning loop that turns every conversation into fine-tuning data.**

---

## What Is Hermes Agent?

Hermes Agent is the successor to OpenClaw — NousResearch's production-grade, self-hosted personal AI agent designed to run 24/7 on your own hardware or cloud infrastructure. With 65,972 GitHub stars and an MIT license, it represents the current state of the art in open-source agent frameworks that combine a richly layered memory system, a multi-platform messaging gateway, and a reinforcement-learning pipeline that continuously improves the underlying models through real usage.

Unlike ephemeral chatbot wrappers, Hermes is built around three design principles:

1. **Continuity** — sessions persist, memories accumulate, skills compound. The agent you run today is smarter than the one you ran last week.
2. **Reach** — one agent, 20+ platforms. Whether you message through Telegram, Discord, Slack, WhatsApp, Signal, Email, Matrix, Feishu, DingTalk, or a raw webhook, the same memory and skill set is available.
3. **Closed learning** — every real interaction is a potential training example. `trajectory.py` records tool calls and outcomes in Atropos RL format; those trajectories can be fed directly into NousResearch's fine-tuning pipeline to improve future model behavior.

---

## Current Snapshot (auto-updated)

- repository: [`nousresearch/hermes-agent`](https://github.com/nousresearch/hermes-agent)
- stars: about **120k**
- latest release: [`v2026.4.23`](https://github.com/nousresearch/hermes-agent/releases/tag/v2026.4.23) (published 2026-04-23)

## Who Should Read This Tutorial

| Audience | What You Will Get |
|---|---|
| Individual developers | A self-hosted AI assistant with memory that actually persists across sessions |
| Platform builders | A messaging gateway you can point at any of 20+ chat platforms with a single config |
| ML researchers | A live data-generation pipeline producing Atropos-format RL trajectories from real agent interactions |
| DevOps / infra engineers | Six swappable terminal backends (local, Docker, SSH, Daytona, Singularity, Modal) for isolated task execution |
| OpenClaw users | A clear migration path: `hermes claw migrate` imports your memories, skills, and config |

---

## Architecture at a Glance

```
cli.py
└── hermes_cli/
    ├── agent/               # LLM core
    │   ├── prompt_builder.py
    │   ├── context_engine.py
    │   ├── memory_manager.py
    │   ├── skill_utils.py
    │   ├── trajectory.py
    │   └── smart_routing.py
    ├── gateway/             # 20+ platform messaging
    │   ├── telegram.py
    │   ├── discord.py
    │   ├── slack.py
    │   ├── whatsapp.py
    │   ├── signal.py
    │   ├── email.py
    │   ├── matrix.py
    │   ├── api_server.py
    │   └── ...
    ├── cron/                # Scheduler + jobs
    │   ├── scheduler.py
    │   └── jobs/
    ├── environments/        # RL training, benchmarks, subagents
    │   ├── hermes_swe_env/
    │   ├── tblite/
    │   └── batch_runner.py
    └── acp_adapter/         # Agent Communication Protocol server
```

---

## Three Memory Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Memory Architecture                   │
├──────────────┬──────────────────┬───────────────────────┤
│   Episodic   │    Semantic      │     Procedural        │
│              │                  │                       │
│ FTS5 SQLite  │  MEMORY.md       │  SKILL.md files       │
│ session      │  USER.md         │  (auto-created and    │
│ search +     │  Honcho user     │   self-improved by    │
│ LLM summary  │  modeling        │   the agent)          │
│ injection    │  (dialectic)     │                       │
└──────────────┴──────────────────┴───────────────────────┘
```

---

## Chapters in This Tutorial

| Chapter | Title | Key Topics |
|---|---|---|
| 1 | [Getting Started](./01-getting-started.md) | Install, `hermes setup`, `~/.hermes/` layout, first conversation, OpenClaw migration |
| 2 | [The TUI and Conversation Interface](./02-tui-and-conversation-interface.md) | curses UI, slash commands, SOUL.md persona, context files, skin system |
| 3 | [Agent Core: Prompt Building, Context Engine, Model Routing](./03-agent-core-prompt-context-routing.md) | prompt_builder.py, context_engine.py, smart_model_routing.py, credential_pool.py |
| 4 | [Memory, Skills, and the Learning Loop](./04-memory-skills-learning-loop.md) | Three memory layers, memory_manager.py, FTS5, Honcho, SKILL.md, agentskills.io |
| 5 | [The Messaging Gateway](./05-messaging-gateway.md) | 20+ platform drivers, session routing, delivery pipeline, API server mode |
| 6 | [Cron Scheduling, Subagents, and Automation](./06-cron-subagents-automation.md) | scheduler.py, cron commands, subagent spawning, terminal backends |
| 7 | [RL Training and Trajectory Generation](./07-rl-training-trajectory.md) | trajectory.py, Atropos, benchmark envs, tool-call parsers, data pipeline |
| 8 | [ACP, MCP, Migration, and Ecosystem](./08-acp-mcp-migration-ecosystem.md) | ACP server, MCP integration, agentskills.io, OpenClaw migration, Nix/Docker deploy |

---

## Quick-Start (TL;DR)

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/nousresearch/hermes-agent/main/install.sh | bash

# Run setup wizard
hermes setup

# Start the TUI
hermes
```

---

## Key Differentiators vs Other Agent Frameworks

| Feature | Hermes Agent | LangChain | AutoGPT | CrewAI |
|---|---|---|---|---|
| Persistent episodic memory (FTS5) | Yes | Plugin-dependent | Partial | No |
| Autonomous skill creation | Yes | No | No | No |
| 20+ platform gateway | Yes | No | No | No |
| RL trajectory generation | Yes | No | No | No |
| Closed fine-tuning loop | Yes | No | No | No |
| Self-hosted, MIT license | Yes | Yes | AGPL | MIT |
| Six terminal backends | Yes | No | No | No |
| ACP multi-agent protocol | Yes | No | No | No |

---

## License and Attribution

Hermes Agent is released under the [MIT License](https://github.com/nousresearch/hermes-agent/blob/main/LICENSE) by NousResearch. This tutorial is an independent educational resource; it is not officially affiliated with NousResearch.
