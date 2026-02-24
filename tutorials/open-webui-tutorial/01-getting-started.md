---
layout: default
title: "Open WebUI Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 1: Getting Started with Open WebUI

Welcome to **Chapter 1: Getting Started with Open WebUI**. In this part of **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy your own ChatGPT alternative with Open WebUI - self-hosted, privacy-focused, and feature-rich.

## Installation Options

### Docker Installation (Recommended)

The easiest way to get started is using Docker:

```bash
# Pull the latest image
docker pull ghcr.io/open-webui/open-webui:latest

# Run with basic configuration
docker run -d \
  --name open-webui \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --restart unless-stopped \
  ghcr.io/open-webui/open-webui:latest
```

Access Open WebUI at `http://localhost:3000`

### Docker Compose (Production Ready)

For a more robust setup with persistent data and environment configuration:

```yaml
# docker-compose.yml
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - open-webui-data:/app/backend/data
    environment:
      - WEBUI_SECRET_KEY=your-secret-key-here
      - OPENAI_API_KEY=your-openai-key
    restart: unless-stopped

volumes:
  open-webui-data:
```

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f open-webui
```

### Manual Installation

For development or custom deployments:

```bash
# Clone the repository
git clone https://github.com/open-webui/open-webui.git
cd open-webui

# Install dependencies
npm install
npm run build

# Install Python backend
cd backend
pip install -r requirements.txt

# Run the application
bash start.sh
```

## First Login and Setup

1. **Access the Web Interface**
   - Open `http://localhost:3000` in your browser
   - You'll see the welcome screen

2. **Initial Configuration**
   ```bash
   # Set admin credentials on first login
   Username: admin
   Password: (set your password)
   ```

3. **Basic Settings**
   - Go to Settings (⚙️) > Account
   - Configure your preferences
   - Set up API keys for external services

## Connecting Your First Model

### Option 1: OpenAI API

```python
# In Open WebUI Settings > Connections
# Add OpenAI API Key
OPENAI_API_KEY=sk-your-key-here

# Select models to enable
- gpt-4
- gpt-4-turbo
- gpt-3.5-turbo
```

### Option 2: Local Ollama Models

First, install Ollama:

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

Pull and run models:

```bash
# Pull a model
ollama pull llama2:7b

# Start Ollama server
ollama serve
```

In Open WebUI:
- Settings > Connections > Ollama
- API Base URL: `http://localhost:11434`
- The models will auto-discover

### Option 3: Other Backends

**Anthropic Claude:**
```
ANTHROPIC_API_KEY=your-key-here
Models: claude-3-opus, claude-3-sonnet, claude-3-haiku
```

**Google Gemini:**
```
GOOGLE_API_KEY=your-key-here
Models: gemini-pro, gemini-pro-vision
```

**LocalAI:**
```bash
# Run LocalAI server first
docker run -p 8080:8080 localai/localai:latest

# Then configure in Open WebUI
API Base URL: http://localhost:8080
```

## Your First Conversation

1. **Select a Model**
   - Click the model selector in the top-left
   - Choose your preferred model (e.g., GPT-4, Llama2)

2. **Start Chatting**
   ```
   User: Hello! Can you help me understand how Open WebUI works?
   Assistant: I'd be happy to help you understand Open WebUI! It's a self-hosted web interface for Large Language Models that provides...
   ```

3. **Explore Features**
   - Try different models
   - Use the sidebar for chat history
   - Experiment with the settings

## Basic Configuration

### Environment Variables

Create a `.env` file for configuration:

```bash
# Security
WEBUI_SECRET_KEY=your-very-long-random-secret-key-here

# OpenAI
OPENAI_API_KEY=sk-your-openai-key
OPENAI_API_BASE_URL=https://api.openai.com/v1

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-key

# Ollama
OLLAMA_BASE_URL=http://localhost:11434

# WebUI Settings
WEBUI_NAME=Your Custom Name
WEBUI_URL=http://localhost:3000
ENABLE_SIGNUP=false
```

### Docker with Environment File

```yaml
# docker-compose.yml with env file
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    env_file:
      - .env
    ports:
      - "3000:8080"
    volumes:
      - ./data:/app/backend/data
    restart: unless-stopped
```

## Troubleshooting Common Issues

### Connection Issues

**Ollama not connecting:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve

# Check Open WebUI logs
docker logs open-webui
```

**API Key Issues:**
```bash
# Test OpenAI API directly
curl -H "Authorization: Bearer sk-your-key" \
     -H "Content-Type: application/json" \
     https://api.openai.com/v1/models
```

### Port Conflicts

```bash
# Find what's using port 3000
lsof -i :3000

# Change port in docker-compose.yml
ports:
  - "3001:8080"
```

### Permission Issues

```bash
# Fix Docker volume permissions
sudo chown -R 1000:1000 ./data

# Or run container as current user
docker run --user $(id -u):$(id -g) ...
```

## Next Steps

Now that you have Open WebUI running, let's explore:

- **[Chapter 2: Model Management](02-model-management.md)** - Connect multiple backends and manage models
- **[Chapter 3: Interface Customization](03-interface-customization.md)** - Personalize your chat experience

## Quick Start Checklist

- [ ] Install Docker or Ollama
- [ ] Run Open WebUI container
- [ ] Access web interface
- [ ] Set admin password
- [ ] Connect at least one model
- [ ] Send your first message
- [ ] Explore basic settings

You're now ready to explore the full power of self-hosted AI chat interfaces! 🚀

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- tutorial slug: **open-webui-tutorial**
- chapter focus: **Chapter 1: Getting Started with Open WebUI**
- system context: **Open Webui Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 1: Getting Started with Open WebUI`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [Open WebUI Repository](https://github.com/open-webui/open-webui)
- [Open WebUI Releases](https://github.com/open-webui/open-webui/releases)
- [Open WebUI Docs](https://docs.openwebui.com/)

### Cross-Tutorial Connection Map

- [Ollama Tutorial](../ollama-tutorial/)
- [LiteLLM Tutorial](../litellm-tutorial/)
- [Langfuse Tutorial](../langfuse-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 1: Getting Started with Open WebUI`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

### Scenario Playbook 1: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 1: Getting Started with Open WebUI

- tutorial context: **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `open`, `webui`, `docker` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Open WebUI` as an operating subsystem inside **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `your`, `latest`, `WebUI` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Open WebUI` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `open`.
2. **Input normalization**: shape incoming data so `webui` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `docker`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Open WebUI Repository](https://github.com/open-webui/open-webui)
  Why it matters: authoritative reference on `Open WebUI Repository` (github.com).
- [Open WebUI Releases](https://github.com/open-webui/open-webui/releases)
  Why it matters: authoritative reference on `Open WebUI Releases` (github.com).
- [Open WebUI Docs](https://docs.openwebui.com/)
  Why it matters: authoritative reference on `Open WebUI Docs` (docs.openwebui.com).

Suggested trace strategy:
- search upstream code for `open` and `webui` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Model Management & Backend Configuration](02-model-management.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
