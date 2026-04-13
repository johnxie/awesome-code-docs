---
layout: default
title: "Chapter 8: Production Deployment and Advanced Patterns"
parent: "DeerFlow Tutorial"
nav_order: 8
format_version: v2
why: "Running DeerFlow in production requires careful attention to sandbox security, checkpointer persistence, observability, resource sizing, and authentication. The default dev configuration is insecure and not suitable for multi-user deployments."
mental_model: "A production DeerFlow deployment is: Nginx (entry point) + LangGraph Platform (agent runtime with Postgres checkpointer) + FastAPI Gateway (support services) + Next.js (UI) + Docker sandbox containers (isolated code execution). Each component has specific production requirements that differ from the development defaults."
learning_outcomes:
  - Deploy DeerFlow with Docker Compose in a production-hardened configuration
  - Configure Postgres checkpointer for persistent thread state across restarts
  - Enable LangSmith or Langfuse observability for all LLM calls
  - Secure the deployment with authentication and network isolation
  - Configure resource sizing for different workload profiles
  - Implement health checks and understand recovery patterns
snapshot:
  repo: bytedance/deer-flow
  stars: ~53.5k
  last_checked: 2026-04-12
chapter_map:
  - "01: Installation and first query"
  - "02: LangGraph state machine internals"
  - "03: Research pipeline deep dive"
  - "04: RAG and search tools"
  - "05: Frontend and API design"
  - "06: Skills and extensions"
  - "07: Podcast and multi-modal outputs"
  - "08 (this): Production deployment"
sources:
  - https://github.com/bytedance/deer-flow/blob/main/backend/docs/ARCHITECTURE.md
  - https://github.com/bytedance/deer-flow/blob/main/backend/docs/SETUP.md
  - https://github.com/bytedance/deer-flow/blob/main/backend/Dockerfile
  - https://github.com/bytedance/deer-flow/.env.example
  - https://github.com/bytedance/deer-flow/blob/main/Makefile
---

# Chapter 8: Production Deployment and Advanced Patterns

## What Problem Does This Solve?

The `make dev` local setup is designed for a single developer with direct host access. Production deployments face different requirements:
- **Multi-user access**: multiple users submitting research tasks concurrently
- **State persistence**: thread history and memory must survive service restarts
- **Security**: untrusted user inputs must not escape the sandbox; the API must require authentication
- **Observability**: you need to know when agent runs fail, which LLM calls are expensive, and where latency is concentrated
- **Resource control**: long-running research jobs must not starve other users
- **Reliability**: the system must recover from sandbox container crashes, LLM API rate limits, and network failures

This chapter covers each of these production concerns with concrete configuration examples.

## How it Works Under the Hood

### Production Architecture

```mermaid
graph TB
    subgraph "Load Balancer / Auth"
        LB[HTTPS Load Balancer<br/>TLS termination<br/>Authentication gateway]
    end

    subgraph "Application Layer"
        N[Nginx :2026<br/>Internal routing]
        LG[LangGraph Server :2024<br/>AioSandboxProvider<br/>Postgres checkpointer]
        GW[Gateway API :8001<br/>FastAPI]
        FE[Next.js :3000]
    end

    subgraph "Sandbox Layer"
        SB1[Docker Sandbox<br/>Thread 1]
        SB2[Docker Sandbox<br/>Thread 2]
        SBN[Docker Sandbox<br/>Thread N]
    end

    subgraph "Persistence Layer"
        PG[PostgreSQL<br/>Thread state + checkpoints]
        FS[Shared Filesystem / S3<br/>Artifacts, uploads, outputs]
    end

    subgraph "Observability"
        LS[LangSmith / Langfuse<br/>LLM call tracing]
        LOG[Centralized Logging<br/>stdout → aggregator]
    end

    LB --> N
    N --> LG
    N --> GW
    N --> FE
    LG --> SB1
    LG --> SB2
    LG --> SBN
    LG --> PG
    GW --> PG
    LG --> FS
    GW --> FS
    LG --> LS
```

### Deployment Sizing

ByteDance documents three deployment profiles:

| Profile | CPU | RAM | Disk | Use Case |
|:--|:--|:--|:--|:--|
| Local eval | 4 vCPU | 8 GB | 20 GB SSD | Single developer testing |
| Docker dev | 4 vCPU | 8 GB | 25 GB SSD | Team dev environment |
| Production server | 8–16 vCPU | 16–32 GB | 40+ GB SSD | Multi-user production |

The large RAM requirement comes from:
- LangGraph server keeping active thread states in memory
- Docker sandbox containers (each uses ~256 MB–1 GB)
- LLM context windows being processed (long research contexts can use GB of memory during inference)

### Production Docker Compose

A production-ready Docker Compose configuration:

```yaml
# docker-compose.prod.yml
version: "3.9"

services:
  nginx:
    image: nginx:1.25-alpine
    ports:
      - "2026:2026"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - langgraph
      - gateway
      - frontend
    restart: unless-stopped

  langgraph:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - LANGGRAPH_POSTGRES_URI=postgresql://deerflow:${DB_PASSWORD}@postgres:5432/deerflow
      - DEER_FLOW_CONFIG_PATH=/app/config.yaml
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_API_KEY=${LANGSMITH_API_KEY}
      - LANGCHAIN_PROJECT=deer-flow-production
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - user_data:/mnt/user-data
      - ./skills:/mnt/skills:ro
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "8"
          memory: 16G

  gateway:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: gateway
    environment:
      - DEER_FLOW_CONFIG_PATH=/app/config.yaml
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - user_data:/mnt/user-data
      - ./extensions_config.json:/app/extensions_config.json
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - NEXT_PUBLIC_API_URL=http://nginx:2026
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: deerflow
      POSTGRES_USER: deerflow
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U deerflow"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  sandbox:
    image: bytedance/deer-flow-sandbox:latest
    volumes:
      - user_data:/mnt/user-data
    deploy:
      replicas: 4     # Pre-warm 4 sandbox containers
      resources:
        limits:
          cpus: "2"
          memory: 2G

volumes:
  postgres_data:
  user_data:
```

### Postgres Checkpointer

The development setup uses SQLite for checkpointing. Production must use Postgres for:
- Persistence across service restarts
- Concurrent access from multiple LangGraph server instances
- Efficient state queries for thread history

```python
# backend/packages/harness/deerflow/agents/checkpointer/async_provider.py
import os
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

def make_checkpointer():
    postgres_uri = os.environ.get("LANGGRAPH_POSTGRES_URI")
    
    if postgres_uri:
        # Production: use Postgres
        return AsyncPostgresSaver.from_conn_string(postgres_uri)
    else:
        # Development: fall back to SQLite
        from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
        return AsyncSqliteSaver.from_conn_string("./checkpoints.db")
```

### Gateway Mode: Eliminating LangGraph Platform Dependency

DeerFlow's "gateway mode" embeds the agent runtime inside the FastAPI Gateway API, reducing the process count from 4 to 3 and removing the LangGraph Platform server:

```python
# backend/app/gateway/app.py (gateway mode)
# In gateway mode, the FastAPI app hosts the agent runtime directly

from deerflow.agents import make_lead_agent
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

app = FastAPI(title="DeerFlow Gateway + Agent Runtime")

@app.on_event("startup")
async def startup():
    checkpointer = AsyncPostgresSaver.from_conn_string(settings.POSTGRES_URI)
    app.state.agent = make_lead_agent()

@app.post("/threads/{thread_id}/runs")
async def run_agent(thread_id: str, request: RunRequest):
    """SSE streaming endpoint for agent execution."""
    async def generate():
        async for event in app.state.agent.astream_events(
            request.input,
            config={"configurable": {"thread_id": thread_id}},
            version="v2",
        ):
            yield f"data: {json.dumps(event)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

Enable gateway mode in the environment:

```bash
DEERFLOW_GATEWAY_MODE=true
```

Gateway mode is marked experimental but is the recommended approach for deployments that want to avoid the LangGraph Platform licensing and process overhead.

### LangSmith Observability

LangSmith provides per-call tracing for all LLM invocations and tool calls:

```bash
# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=deer-flow-production
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com  # default
```

With tracing enabled, every research run creates a trace with:
- Full message history at each step
- Tool call inputs and outputs
- Token counts and costs per LLM call
- Latency at each node
- Error stacks for failed runs

```mermaid
graph LR
    A[LangGraph Agent Run] --> B[LangSmith Trace]
    B --> C[Run overview<br/>total tokens, cost, latency]
    B --> D[Per-step spans<br/>each LLM call + tool call]
    B --> E[Input/output at each step]
    B --> F[Error details if failed]
```

### Langfuse: Open-Source Alternative

For teams that cannot send data to LangSmith (data residency requirements), Langfuse is an open-source observability alternative:

```bash
# .env
LANGFUSE_HOST=https://cloud.langfuse.com  # or self-hosted
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
```

```python
# backend/packages/harness/deerflow/agents/lead_agent/agent.py
# Langfuse integration (conceptual — actual config is via env vars)
from langfuse.callback import CallbackHandler

langfuse_handler = CallbackHandler()

# Injected into agent config:
config = {
    "callbacks": [langfuse_handler],
    "configurable": {"thread_id": thread_id},
}
```

### Security Hardening

**1. Sandbox isolation** — always use `AioSandboxProvider` (Docker) in production:

```yaml
# config.yaml
sandbox:
  use: deerflow.community.aio_sandbox:AioSandboxProvider
  allow_host_bash: false    # NEVER true in production
  auto_start: true
  container_prefix: deer-flow-sandbox
```

The sandbox provides:
- Filesystem isolation (agent code cannot reach host files outside `/mnt/user-data`)
- Network isolation (configurable — default allows outbound for web search)
- Resource limits per container (CPU and memory caps)

**2. Authentication** — DeerFlow defaults to no auth. Add authentication at Nginx:

```nginx
# nginx.conf (production auth example using OAuth2 Proxy)
location / {
    auth_request /oauth2/auth;
    error_page 401 = /oauth2/sign_in;
    proxy_pass http://frontend:3000;
}

location /oauth2/ {
    proxy_pass http://oauth2-proxy:4180;
}
```

Or use the built-in `better-auth` integration in the frontend:

```typescript
// frontend/src/server/better-auth/config.ts
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";

export const auth = betterAuth({
    database: prismaAdapter(prisma, { provider: "postgresql" }),
    socialProviders: {
        github: {
            clientId: process.env.GITHUB_CLIENT_ID!,
            clientSecret: process.env.GITHUB_CLIENT_SECRET!,
        },
        google: {
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
        },
    },
});
```

**3. Network exposure** — DeerFlow's documentation states:

> "DeerFlow is designed for local trusted deployments. Untrusted network exposure requires IP allowlists, authentication gateways, and network isolation to prevent unauthorized agent invocation and potential abuse."

Never expose the LangGraph server port (`:2024`) or Gateway API port (`:8001`) directly to the internet. Route all traffic through Nginx or a load balancer with authentication.

### Health Checks and Monitoring

Configure health checks for each service:

```yaml
# docker-compose.prod.yml health checks
services:
  langgraph:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:2024/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  gateway:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 5s
      retries: 3
```

The `make doctor` script can also be run as a scheduled health check:

```bash
# Cron: run doctor every 5 minutes, alert if it fails
*/5 * * * * cd /opt/deer-flow && make doctor >> /var/log/deerflow-health.log 2>&1
```

### Recovery Patterns

**LLM API Rate Limits:**

DeerFlow's `LLMErrorHandlingMiddleware` handles rate limit responses from LLM providers with exponential backoff. No additional configuration is needed, but you should monitor LangSmith/Langfuse for runs that are slow due to rate limit retries.

**Sandbox Container Crashes:**

If a Docker sandbox container crashes mid-execution:
1. `SandboxMiddleware` detects the missing container ID in `ThreadState.sandbox`
2. A new container is provisioned for the thread on the next invocation
3. The agent resumes from the last checkpoint (previous messages are intact)
4. Files in the workspace directory persist (they are on the shared volume, not inside the container)

**LangGraph Server Restart:**

With Postgres checkpointer:
- All thread states are persisted and immediately available after restart
- In-flight runs at the time of restart are marked as failed
- Users can resubmit their last message to resume from the last saved checkpoint

**Disk Full:**

Generated artifacts (MP3s, PDFs, slides) accumulate on the shared volume. Implement periodic cleanup:

```python
# scripts/cleanup_old_threads.py
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

OUTPUTS_DIR = Path("/mnt/user-data/outputs")
RETENTION_DAYS = 30

def cleanup_old_outputs():
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    
    for thread_dir in OUTPUTS_DIR.iterdir():
        if thread_dir.is_dir():
            mtime = datetime.fromtimestamp(thread_dir.stat().st_mtime)
            if mtime < cutoff:
                shutil.rmtree(thread_dir)
                print(f"Deleted: {thread_dir}")

if __name__ == "__main__":
    cleanup_old_outputs()
```

### Advanced Pattern: Agent Guardrails

For deployments where you need to restrict what the agent can do (e.g., corporate environments):

```python
# backend/docs/GUARDRAILS.md describes this pattern

# Guardrails are implemented as middleware that intercepts tool calls
class ContentGuardrailMiddleware(BaseMiddleware):
    """Block tool calls to specific domains or with specific patterns."""
    
    BLOCKED_DOMAINS = {"competitor.com", "internal.company.com"}
    
    async def before_tool_call(
        self,
        tool_name: str,
        tool_input: dict,
        state: ThreadState,
    ) -> dict | None:
        """Return None to allow, return error dict to block."""
        
        if tool_name in ("web_search", "web_fetch"):
            url = tool_input.get("url", "")
            query = tool_input.get("query", "")
            
            for domain in self.BLOCKED_DOMAINS:
                if domain in url or domain in query:
                    return {"error": f"Access to {domain} is restricted by policy."}
        
        return None  # Allow the tool call
```

### Cost Management

LLM API costs scale with:
- Number of concurrent users
- Research depth (sub-agent count and search iterations)
- Model selection (o3 vs. gpt-4o-mini cost ratio can be 100x)

Production cost controls:

```yaml
# config.yaml — cost-efficient defaults with premium model available
models:
  - name: gpt-4o-mini
    display_name: GPT-4o Mini (Default)
    use: langchain_openai:ChatOpenAI
    model: gpt-4o-mini
    api_key: $OPENAI_API_KEY

  - name: o3-mini
    display_name: o3 Mini (Deep Research)
    use: langchain_openai:ChatOpenAI
    model: o3-mini
    api_key: $OPENAI_API_KEY
    supports_thinking: true
```

```yaml
# Per-agent config: limit sub-agent parallelism to control costs
# workspace/agents/lead_agent/config.yaml
subagent:
  max_concurrent: 2   # Reduce from default 3 to limit parallel LLM calls
```

## Summary

Production DeerFlow deployment requires:
1. **Postgres checkpointer** for persistent thread state
2. **AioSandboxProvider** (Docker) for isolated code execution
3. **Authentication** at Nginx or via better-auth
4. **LangSmith or Langfuse** for observability
5. **Shared filesystem volume** for artifacts persistence across service restarts
6. **Resource sizing** based on concurrent user count and research depth
7. **Periodic cleanup** for accumulated artifacts
8. **Network isolation** preventing direct exposure of internal service ports

The gateway mode (experimental) simplifies the architecture by embedding the agent runtime in the FastAPI server, reducing the process count and removing the LangGraph Platform dependency.

---

## Tutorial Complete

You have now covered the full DeerFlow system:

- **Chapter 1**: Installation, configuration, and first research query
- **Chapter 2**: LangGraph state machine, 14-stage middleware pipeline, async checkpointing
- **Chapter 3**: Research pipeline — CLARIFY → PLAN → ACT, deep research skill, citations
- **Chapter 4**: RAG and search tools — DuckDuckGo, Tavily, Exa, Firecrawl, sandbox REPL, MCP
- **Chapter 5**: Three-service architecture, SSE streaming, Gateway API, IM channels
- **Chapter 6**: Skills system, custom tools, MCP servers, per-agent config overrides
- **Chapter 7**: Podcast generation, PowerPoint, charts, image and video generation
- **Chapter 8**: Production deployment, Postgres checkpointer, security, observability, cost management

## Further Resources

- [DeerFlow GitHub Repository](https://github.com/bytedance/deer-flow)
- [Architecture Documentation](https://github.com/bytedance/deer-flow/blob/main/backend/docs/ARCHITECTURE.md)
- [Configuration Reference](https://github.com/bytedance/deer-flow/blob/main/backend/docs/CONFIGURATION.md)
- [Skills Library](https://github.com/bytedance/deer-flow/tree/main/skills/public)
- [Contributing Guide](https://github.com/bytedance/deer-flow/blob/main/CONTRIBUTING.md)

---

## Chapter Connections

- [Tutorial Index](README.md)
- [Previous Chapter: Chapter 7: Podcast and Multi-Modal Output](07-podcast-multimodal.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
