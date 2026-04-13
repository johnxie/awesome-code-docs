---
layout: default
title: "Chapter 8: ACP, MCP, Migration, and Ecosystem"
nav_order: 8
parent: Hermes Agent Tutorial
format_version: v2
why: "Hermes is not an island. Understanding how it participates in multi-agent networks via ACP, exposes itself as an MCP server, integrates with the agentskills.io ecosystem, and deploys reproducibly via Nix and Docker is essential for building production systems and contributing back to the project."
mental_model: "Hermes at the edges: ACP makes Hermes a node in a multi-agent network; MCP makes Hermes's capabilities available to any MCP client; agentskills.io makes Hermes's learned skills portable; and Nix/Docker make Hermes's deployment reproducible across any machine."
learning_outcomes:
  - Understand the Agent Communication Protocol and configure Hermes's ACP server
  - Set up Hermes as an MCP server for use with Claude Desktop or other MCP clients
  - Migrate from OpenClaw with hermes claw migrate
  - Deploy Hermes with Docker Compose or Nix for reproducible production setups
  - Contribute skills to agentskills.io and understand the project's contribution workflow
snapshot:
  source_repo: https://github.com/nousresearch/hermes-agent
  stars: 65972
  language: Python
  license: MIT
chapter_map:
  - hermes_cli/acp_adapter/
  - hermes_cli/acp_adapter/server.py
  - hermes_cli/gateway/mcp_serve.py
  - hermes_cli/migration/claw.py
  - flake.nix
  - docker-compose.yml
sources:
  - https://github.com/nousresearch/hermes-agent
---

# Chapter 8: ACP, MCP, Migration, and Ecosystem

## What Problem Does This Solve?

Single-agent systems have fundamental limitations: they can only do one thing at a time, they're bottlenecked by one model's capabilities, and they're isolated from other agents that might have complementary skills. Hermes addresses this through two complementary protocols:

- **ACP (Agent Communication Protocol)** makes Hermes a node in a multi-agent network — it can receive tasks from orchestrator agents, spawn peer agents, and report results back through a standardized interface.
- **MCP (Model Context Protocol)** makes Hermes's memory, skills, and execution capabilities available to any MCP-compatible client, including Claude Desktop.

Together with the agentskills.io ecosystem and reproducible deployment options, these integrations position Hermes as a building block in larger AI systems rather than a standalone tool.

---

## ACP — Agent Communication Protocol

### What Is ACP?

The Agent Communication Protocol is an emerging standard for agent-to-agent communication. It defines how agents advertise their capabilities, accept task requests, stream results, and report completion. Hermes implements ACP via the `acp_adapter/` module, which exposes an HTTP/SSE server that any ACP-compatible orchestrator can call.

### ACP Server Architecture

```mermaid
flowchart TD
    subgraph External["External Orchestrators"]
        ORCH1[Orchestrator Agent\ne.g. MetaGPT]
        ORCH2[Orchestrator Agent\ne.g. AutoGen]
        ORCH3[Custom Orchestrator]
    end

    subgraph ACP["hermes_cli/acp_adapter/"]
        SRV[server.py\nHTTP/SSE server]
        CAPS[capabilities.py\nCapability registry]
        TASK[task_handler.py\nTask lifecycle]
        AUTH[auth.py\nAPI key validation]
    end

    subgraph HermesCore["Hermes Core"]
        AGENT[Agent Loop\nprompt_builder + LLM]
        MEM[Memory System]
        TOOLS[Tool Execution]
    end

    ORCH1 -->|POST /agents/hermes/tasks| SRV
    ORCH2 -->|POST /agents/hermes/tasks| SRV
    ORCH3 -->|GET /agents/hermes/capabilities| CAPS
    SRV --> AUTH
    AUTH --> TASK
    TASK --> AGENT
    AGENT --> MEM
    AGENT --> TOOLS
    TASK -->|SSE stream| ORCH1
    TASK -->|SSE stream| ORCH2
```

### ACP Server Configuration

```yaml
# ~/.hermes/config.yaml

acp:
  enabled: true
  host: "0.0.0.0"
  port: 8765
  
  auth:
    api_keys:
      - key: "acp-key-abc123"
        name: "orchestrator-1"
        permissions: [tasks, capabilities, status]
    require_auth: true
  
  capabilities:
    # Which Hermes capabilities to expose via ACP
    expose_memory: true         # Allow reading MEMORY.md / USER.md
    expose_skills: true         # Allow reading and executing skills
    expose_shell: false         # Shell execution (disabled by default for security)
    expose_gateway: false       # Messaging gateway (disabled by default)
    
  rate_limits:
    requests_per_minute: 60
    max_concurrent_tasks: 3
```

### ACP Capability Discovery

An orchestrator can discover Hermes's capabilities before assigning tasks:

```bash
curl http://localhost:8765/agents/hermes/capabilities \
  -H "Authorization: Bearer acp-key-abc123"
```

```json
{
  "agent_id": "hermes",
  "version": "0.4.2",
  "display_name": "Hermes Agent",
  "description": "Self-hosted personal AI agent with persistent memory and skill system",
  "capabilities": [
    {
      "id": "chat",
      "description": "General-purpose conversation with full memory access",
      "input_schema": {"type": "object", "properties": {"message": {"type": "string"}}},
      "output_schema": {"type": "object", "properties": {"response": {"type": "string"}}}
    },
    {
      "id": "skill_execution",
      "description": "Execute a named skill from the skill library",
      "input_schema": {"type": "object", "properties": {"skill_id": {"type": "string"}, "context": {"type": "string"}}}
    },
    {
      "id": "memory_query",
      "description": "Query episodic or semantic memory",
      "input_schema": {"type": "object", "properties": {"query": {"type": "string"}, "layer": {"type": "string", "enum": ["episodic", "semantic", "procedural"]}}}
    }
  ]
}
```

### Sending a Task to Hermes via ACP

```python
import requests
import json

# Assign a task to Hermes from an orchestrator
response = requests.post(
    "http://localhost:8765/agents/hermes/tasks",
    headers={"Authorization": "Bearer acp-key-abc123"},
    json={
        "task_id": "task-001",
        "capability": "chat",
        "input": {
            "message": "Summarize the current state of the data-pipeline-v2 project from your memory."
        },
        "stream": True  # Request SSE streaming
    },
    stream=True
)

# Consume the SSE stream
for line in response.iter_lines():
    if line.startswith(b"data:"):
        event = json.loads(line[5:])
        if event["type"] == "token":
            print(event["content"], end="", flush=True)
        elif event["type"] == "complete":
            print("\nTask complete.")
            break
```

### ACP Task Lifecycle

```mermaid
sequenceDiagram
    participant Orch as Orchestrator
    participant ACP as acp_adapter/server.py
    participant TH as task_handler.py
    participant Agent as Hermes Agent

    Orch->>ACP: POST /agents/hermes/tasks
    ACP->>ACP: validate API key
    ACP->>TH: create_task(task_request)
    TH-->>Orch: 202 Accepted {task_id}
    
    TH->>Agent: run(capability, input)
    
    loop streaming
        Agent-->>TH: partial response token
        TH-->>Orch: SSE event {type: "token", content: "..."}
    end
    
    Agent-->>TH: complete response
    TH->>TH: record trajectory
    TH-->>Orch: SSE event {type: "complete", result: {...}}
    
    Orch->>ACP: GET /agents/hermes/tasks/{task_id}
    ACP-->>Orch: task status and full result
```

---

## MCP — Model Context Protocol

### What Is MCP?

The Model Context Protocol is Anthropic's open standard for giving AI assistants access to external tools and data sources. By running `hermes gateway mcp-serve`, Hermes exposes its memory system, skill library, and execution capabilities as an MCP server that any MCP-compatible client can connect to — including Claude Desktop.

### Starting the MCP Server

```bash
# Start Hermes as an MCP server
hermes gateway mcp-serve --port 3001

# Or run in the background
hermes gateway mcp-serve --port 3001 &
```

### Connecting Claude Desktop to Hermes

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["gateway", "mcp-serve", "--stdio"],
      "env": {
        "HERMES_HOME": "/Users/yourname/.hermes"
      }
    }
  }
}
```

### Exposed MCP Tools

```python
# hermes_cli/gateway/mcp_serve.py (tool definitions)

MCP_TOOLS = [
    {
        "name": "hermes_memory_search",
        "description": "Search Hermes's episodic memory for relevant past sessions",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "hermes_skill_list",
        "description": "List all skills in the Hermes skill library",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "hermes_skill_get",
        "description": "Retrieve the full content of a named skill",
        "input_schema": {
            "type": "object",
            "properties": {
                "skill_id": {"type": "string"}
            },
            "required": ["skill_id"]
        }
    },
    {
        "name": "hermes_chat",
        "description": "Send a message to the Hermes agent (with full memory access)",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "session_id": {"type": "string", "description": "Optional: continue an existing session"}
            },
            "required": ["message"]
        }
    }
]
```

### mcp_serve.py Architecture

```mermaid
flowchart TD
    subgraph MCPClients["MCP Clients"]
        CD[Claude Desktop]
        CC[Claude Code]
        CUSTOM[Custom MCP Client]
    end

    subgraph MCPServer["hermes_cli/gateway/mcp_serve.py"]
        PROTO[MCP Protocol Handler\nJSON-RPC / stdio / SSE]
        TOOLS[Tool Registry\nhermes_memory_search\nhermes_skill_list\nhermes_skill_get\nhermes_chat]
        EXEC[Tool Executor]
    end

    subgraph HermesCore["Hermes Core"]
        CE[context_engine.py\nFTS5 search]
        SK[skill_utils.py\nSkill library]
        AG[Agent Core\nfull chat loop]
    end

    CD -->|stdio| PROTO
    CC -->|stdio| PROTO
    CUSTOM -->|SSE| PROTO
    PROTO --> TOOLS
    TOOLS --> EXEC
    EXEC --> CE
    EXEC --> SK
    EXEC --> AG
```

---

## OpenClaw Migration

`hermes claw migrate` is the comprehensive migration tool for users coming from OpenClaw (Hermes's predecessor).

### Migration Flow

```mermaid
flowchart TD
    A[hermes claw migrate] --> B[detect ~/.openclaw/]
    B --> C{found?}
    C -->|no| D[error: ~/.openclaw not found]
    C -->|yes| E[inventory OpenClaw data]
    E --> F[show migration preview to user]
    F --> G{user confirms?}
    G -->|no| H[exit]
    G -->|yes| I[migrate sessions]
    I --> J[migrate skills]
    J --> K[merge MEMORY.md]
    K --> L[merge USER.md]
    L --> M[translate config.yaml]
    M --> N[verify migration integrity]
    N --> O{issues found?}
    O -->|yes| P[show issues, offer fixes]
    O -->|no| Q[migration complete]
    P --> Q
```

### Migration Details

```bash
hermes claw migrate --dry-run     # Preview what would be migrated
hermes claw migrate               # Perform migration
hermes claw migrate --keep-source # Don't move files, just copy
```

**Sessions:** OpenClaw's session format is translated to Hermes's FTS5 schema. The session content is re-summarized if the original summary doesn't meet Hermes's minimum quality threshold.

**Skills:** SKILL.md format is identical between OpenClaw and Hermes — files are copied directly.

**MEMORY.md merging:** If both `~/.openclaw/MEMORY.md` and `~/.hermes/MEMORY.md` exist, a semantic deduplication pass removes duplicate facts before merging.

**Config translation:**

| OpenClaw Key | Hermes Equivalent |
|---|---|
| `model.primary` | `llm.model` |
| `model.api_key` | `llm.api_key` |
| `execution.mode` | `execution.backend` |
| `memory.episodic.enabled` | `memory.episodic.enabled` |
| `plugins.telegram` | `gateway.platforms.telegram` |

---

## Production Deployment

### Docker Compose

```yaml
# docker-compose.yml (reference)

version: "3.9"

services:
  hermes:
    image: nousresearch/hermes-agent:latest
    # Or build from source:
    # build: .
    
    volumes:
      - ~/.hermes:/home/hermes/.hermes    # Persist all state
      - ~/.ssh:/home/hermes/.ssh:ro       # For SSH backend
    
    environment:
      - HERMES_API_KEY=${HERMES_API_KEY}
      - HERMES_HOME=/home/hermes/.hermes
    
    ports:
      - "8080:8080"    # Gateway API server
      - "8765:8765"    # ACP server
      - "3001:3001"    # MCP server
    
    restart: unless-stopped
    
    # For Docker-in-Docker (Docker terminal backend inside Docker)
    # volumes:
    #   - /var/run/docker.sock:/var/run/docker.sock

  # Optional: Honcho user modeling service
  honcho:
    image: nousresearch/honcho:latest
    environment:
      - DATABASE_URL=postgresql://honcho:honcho@postgres/honcho
    depends_on:
      - postgres

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=honcho
      - POSTGRES_PASSWORD=honcho
      - POSTGRES_DB=honcho
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
# Deploy
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f hermes

# Update
docker compose pull && docker compose up -d
```

### Nix

For maximum reproducibility, Hermes ships with a `flake.nix` that pins every dependency:

```bash
# Enter development shell
nix develop

# Build the package
nix build

# Run directly
nix run github:nousresearch/hermes-agent

# Install to system profile
nix profile install github:nousresearch/hermes-agent
```

The Nix flake provides:
- A reproducible development environment (exact Python version, all dependencies)
- A derivation for building Hermes as a Nix package
- NixOS module for declarative system-level deployment

```nix
# NixOS module usage example
{
  services.hermes-agent = {
    enable = true;
    hermesHome = "/var/lib/hermes";
    user = "hermes-agent";
    
    settings = {
      llm.provider = "openai";
      llm.model = "gpt-4o";
      gateway.platforms.telegram.enabled = true;
    };
    
    secrets = {
      apiKeyFile = config.age.secrets.hermes-api-key.path;
    };
  };
}
```

---

## agentskills.io Integration

`agentskills.io` is the community platform for sharing SKILL.md files. Hermes has first-class integration:

```bash
# Search for skills
hermes skills search "kubernetes deployment"

# Install a community skill
hermes skills install kubernetes-deployment-patterns

# Publish your skill
hermes skills publish python_etl_patterns \
  --description "Battle-tested Python ETL patterns for Airflow" \
  --tags "python,etl,airflow,data-engineering"

# Update a published skill
hermes skills publish python_etl_patterns --update

# Rate a skill
hermes skills rate kubernetes-deployment-patterns --stars 5
```

### Skill Publication Requirements

To publish to agentskills.io, a skill must:
1. Have complete YAML frontmatter (skill_id, description, tags, tested_with)
2. Include a "When to Use This Skill" section
3. Include at least one concrete code example
4. Not contain sensitive information (API keys, personal data)
5. Be under 50KB

---

## Contributing to Hermes Agent

### Repository Structure for Contributors

```
hermes-agent/
├── hermes_cli/          # Main package
│   ├── agent/           # Core agent logic
│   ├── gateway/         # Platform adapters
│   ├── cron/            # Scheduler
│   ├── environments/    # Benchmarks and execution
│   └── acp_adapter/     # ACP server
├── tests/               # Test suite
│   ├── unit/
│   ├── integration/
│   └── benchmarks/
├── docs/                # Documentation
├── flake.nix            # Nix flake
├── docker-compose.yml   # Docker Compose
└── pyproject.toml       # Python package config
```

### Development Setup

```bash
git clone https://github.com/nousresearch/hermes-agent.git
cd hermes-agent

# With Nix (recommended)
nix develop

# With uv
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest tests/unit/
pytest tests/integration/  # Requires API keys in environment

# Run a specific benchmark
python -m hermes_cli.environments.tblite --tasks 10 --model gpt-4o-mini
```

### Adding a New Gateway Platform

```python
# hermes_cli/gateway/myplatform.py

from hermes_cli.gateway.base import BaseAdapter, GatewayMessage

class MyPlatformAdapter(BaseAdapter):
    """Adapter for MyPlatform messaging service."""
    
    platform_name = "myplatform"
    
    async def start(self):
        """Initialize the platform connection."""
        ...
    
    async def handle_incoming(self, raw_event: dict) -> GatewayMessage | None:
        """Convert platform-native event to GatewayMessage."""
        ...
    
    async def send_response(self, chat_id: str, text: str, **kwargs):
        """Send a response to the platform."""
        ...
    
    async def stop(self):
        """Clean up the connection."""
        ...
```

Then register in `hermes_cli/gateway/__init__.py`:

```python
ADAPTERS = {
    # ...existing adapters...
    "myplatform": MyPlatformAdapter,
}
```

---

## Ecosystem Summary

```mermaid
graph TD
    subgraph Hermes["Hermes Agent Core"]
        CORE[Agent Loop\nMemory + Skills]
    end

    subgraph Protocols["Protocol Integrations"]
        ACP[ACP Server\nacp_adapter/\nMulti-agent networks]
        MCP[MCP Server\nmcp_serve.py\nClaude Desktop / Code]
    end

    subgraph Community["Community"]
        SKILLS[agentskills.io\nSkill Hub]
        GH[GitHub\nContributions]
    end

    subgraph Deploy["Deployment"]
        DOCKER[Docker Compose\nProduction deploy]
        NIX[Nix Flake\nReproducible dev + deploy]
        NIXOS[NixOS Module\nDeclarative system config]
    end

    subgraph Migration["Migration"]
        CLAW[hermes claw migrate\nOpenClaw → Hermes]
    end

    CORE <--> ACP
    CORE <--> MCP
    CORE <--> SKILLS
    CORE --> GH
    CORE --> DOCKER
    CORE --> NIX
    NIX --> NIXOS
    CLAW --> CORE
```

---

## Chapter Summary

| Concept | Key Takeaway |
|---|---|
| ACP server | HTTP/SSE server in acp_adapter/; exposes Hermes to multi-agent orchestrators |
| ACP capabilities | Capability discovery endpoint; orchestrators can query what Hermes can do |
| MCP server | mcp_serve.py; exposes memory search, skill library, and chat to MCP clients |
| Claude Desktop | Connect via mcpServers config; use Hermes memory from Claude chat |
| MCP tools | hermes_memory_search, hermes_skill_list, hermes_skill_get, hermes_chat |
| OpenClaw migration | hermes claw migrate; handles sessions, skills, MEMORY.md, USER.md, config |
| Docker Compose | Production deployment; volume-mounts ~/.hermes; runs gateway + ACP + MCP |
| Nix flake | Reproducible dev and deploy; NixOS module for declarative system config |
| agentskills.io | Community skill hub; publish/install/rate skills via hermes skills commands |
| Contributing | Add platform adapters by implementing BaseAdapter; register in gateway/__init__.py |
