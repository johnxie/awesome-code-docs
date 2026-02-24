---
layout: default
title: "Getting Started"
parent: "ElizaOS Deep Dive"
nav_order: 1
---

# Chapter 1: Getting Started with ElizaOS

Welcome to **Chapter 1: Getting Started with ElizaOS**. In this part of **ElizaOS: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


## Introduction

ElizaOS is a TypeScript framework for building autonomous AI agents. Agents can operate across Discord, Telegram, Slack, X/Twitter, and Web3 platforms. They're configured through character files, extended through plugins, and powered by any LLM backend. This chapter covers installation, project setup, and running your first agent.

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Node.js** | 23.x | Latest LTS |
| **Runtime** | Node.js or Bun | Bun (faster) |
| **RAM** | 2 GB | 8 GB+ |
| **Storage** | 1 GB | 5 GB+ |
| **Database** | PGLite (embedded) | PostgreSQL 15+ |

## Installation

### Using the CLI (Recommended)

```bash
# Install the ElizaOS CLI globally
npm install -g @elizaos/cli

# Create a new project
elizaos create my-agent

# Navigate into the project
cd my-agent

# Start in development mode
elizaos dev
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/elizaOS/eliza.git
cd eliza

# Install dependencies with Bun
bun install

# Build all packages
bun run build

# Start the server
bun run start
```

### Docker

```bash
# Using docker-compose
docker compose up -d

# Or build and run directly
docker build -t elizaos .
docker run -d \
  --name elizaos \
  -p 3000:3000 \
  -e OPENAI_API_KEY=sk-... \
  elizaos
```

## Project Structure

A new ElizaOS project:

```
my-agent/
├── src/
│   ├── index.ts           # Entry point
│   ├── character.json     # Agent character definition
│   └── plugins/           # Custom plugins
├── knowledge/             # Documents for RAG
├── .env                   # Environment variables
├── package.json
└── tsconfig.json
```

The ElizaOS monorepo itself:

```
eliza/
├── packages/
│   ├── core/              # AgentRuntime, types, memory, database
│   ├── server/            # Express.js API server
│   ├── client/            # React web dashboard
│   ├── cli/               # elizaos CLI tool
│   ├── app/               # Tauri desktop app
│   ├── api-client/        # Type-safe API client
│   ├── plugin-bootstrap/  # Core plugin (actions, providers)
│   ├── plugin-sql/        # Database adapter
│   ├── plugin-starter/    # Plugin template
│   └── service-interfaces/# Shared service definitions
├── examples/              # Standalone examples
├── docs/                  # Documentation
└── scripts/               # Build utilities
```

## Environment Configuration

```bash
# .env
# LLM Provider (choose one or more)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_GENERATIVE_AI_API_KEY=...

# Database (optional — defaults to PGLite)
DATABASE_URL=postgresql://user:pass@localhost:5432/elizaos

# Platform Connectors (as needed)
DISCORD_APPLICATION_ID=...
DISCORD_API_TOKEN=...
TELEGRAM_BOT_TOKEN=...
TWITTER_USERNAME=...
TWITTER_PASSWORD=...

# Server
SERVER_PORT=3000
```

## Your First Agent

### 1. Define a Character

```json
{
  "name": "Atlas",
  "description": "A helpful AI research assistant",
  "modelProvider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "bio": [
    "Atlas is a research-focused AI assistant that excels at finding information, synthesizing knowledge, and providing clear explanations.",
    "Atlas is thorough but concise, always citing sources when available."
  ],
  "style": {
    "all": [
      "Respond clearly and concisely",
      "Use bullet points for lists",
      "Cite sources when referencing specific facts",
      "Ask clarifying questions when the request is ambiguous"
    ],
    "chat": [
      "Keep responses conversational but informative",
      "Use paragraphs for complex explanations"
    ],
    "post": [
      "Keep posts under 280 characters",
      "Use hashtags sparingly"
    ]
  },
  "topics": [
    "technology",
    "science",
    "programming",
    "AI research"
  ],
  "adjectives": [
    "thorough",
    "analytical",
    "clear",
    "helpful"
  ],
  "knowledge": [],
  "plugins": [
    "@elizaos/plugin-bootstrap",
    "@elizaos/plugin-sql"
  ],
  "settings": {
    "model": "claude-sonnet-4-20250514",
    "embeddingModel": "text-embedding-3-small",
    "maxContextTokens": 128000
  }
}
```

### 2. Create the Entry Point

```typescript
// src/index.ts
import { AgentRuntime, type Character } from "@elizaos/core";
import { bootstrapPlugin } from "@elizaos/plugin-bootstrap";
import { sqlPlugin } from "@elizaos/plugin-sql";
import character from "./character.json";

async function main() {
  // Create the agent runtime
  const runtime = new AgentRuntime({
    character: character as Character,
    plugins: [bootstrapPlugin, sqlPlugin],
  });

  // Initialize the runtime
  await runtime.initialize();

  console.log(`Agent "${character.name}" is running!`);
}

main().catch(console.error);
```

### 3. Run the Agent

```bash
# Development mode (with hot reload)
elizaos dev

# Or production mode
elizaos start
```

### 4. Interact via the Dashboard

Open `http://localhost:3000` to access the React dashboard:

```
┌─────────────────────────────────────┐
│  ElizaOS Dashboard                   │
├─────────────────────────────────────┤
│  Agents: Atlas (online)              │
│                                      │
│  [Chat] [Logs] [Settings] [Plugins]  │
│                                      │
│  You: Tell me about quantum computing│
│                                      │
│  Atlas: Quantum computing uses       │
│  quantum mechanics principles like   │
│  superposition and entanglement to   │
│  process information...              │
└─────────────────────────────────────┘
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `elizaos create <name>` | Scaffold a new project |
| `elizaos dev` | Start in development mode with hot reload |
| `elizaos start` | Start in production mode |
| `elizaos env` | Manage environment configuration |
| `elizaos test` | Run tests for your plugins/agents |
| `elizaos plugin install <name>` | Install a plugin |
| `elizaos plugin list` | List available plugins |

## Understanding the Runtime Flow

```mermaid
sequenceDiagram
    participant User
    participant Connector as Platform Connector
    participant Event as Event Pipeline
    participant Runtime as AgentRuntime
    participant Memory as Memory Store
    participant LLM as Model Provider

    User->>Connector: Send message
    Connector->>Event: Emit MESSAGE_RECEIVED
    Event->>Runtime: Process event
    Runtime->>Memory: Retrieve context
    Memory-->>Runtime: Conversation history + RAG results
    Runtime->>LLM: Generate response
    LLM-->>Runtime: Response + actions
    Runtime->>Event: Emit response events
    Event->>Connector: Deliver response
    Connector->>User: Display response
```

The flow:
1. **Connector** receives a message from a platform (Discord, Telegram, etc.)
2. **Event Pipeline** normalizes it into a platform-agnostic event
3. **AgentRuntime** processes the event, retrieving relevant memories
4. **Model Provider** generates a response (possibly with tool calls)
5. **Response** flows back through the pipeline to the original platform

## Troubleshooting

### Common Issues

```bash
# Port already in use
SERVER_PORT=3001 elizaos start

# Database connection failed (fallback to PGLite)
# Remove DATABASE_URL from .env to use embedded PGLite

# Missing API key
# Ensure at least one LLM provider key is set in .env

# Bun installation issues
npm install -g bun  # Or use Node.js 23+
```

### Debug Logging

```bash
# Enable verbose logging
LOG_LEVEL=debug elizaos dev

# Log specific modules
DEBUG=elizaos:runtime,elizaos:memory elizaos dev
```

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Installation** | `elizaos create` for new projects; Docker for production |
| **Character Files** | JSON definitions for agent personality, style, and capabilities |
| **Plugin System** | Bootstrap + SQL are the minimum plugins; extensible via npm |
| **CLI** | `elizaos dev` for development, `elizaos start` for production |
| **Dashboard** | React web UI at `localhost:3000` for agent management |
| **Model Agnostic** | Set provider via character file; supports OpenAI, Anthropic, etc. |

---

**Next Steps**: [Chapter 2: Agent Runtime](02-agent-runtime.md) — Dive into the AgentRuntime class, lifecycle management, and state processing.

---

*Built with insights from the [ElizaOS repository](https://github.com/elizaOS/eliza) and community documentation.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `elizaos`, `plugin`, `character` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with ElizaOS` as an operating subsystem inside **ElizaOS: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Runtime`, `participant`, `Connector` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with ElizaOS` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `elizaos`.
2. **Input normalization**: shape incoming data so `plugin` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `character`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [ElizaOS](https://github.com/elizaOS/eliza)
  Why it matters: authoritative reference on `ElizaOS` (github.com).

Suggested trace strategy:
- search upstream code for `elizaos` and `plugin` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Agent Runtime](02-agent-runtime.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
