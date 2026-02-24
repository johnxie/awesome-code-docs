---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Devika Tutorial
---

# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter walks through installing Devika, configuring API keys, and running a first autonomous coding task end-to-end.

## Learning Goals

- clone and install Devika with all required system dependencies
- configure LLM provider credentials and environment variables
- launch the Devika web UI and backend services
- submit a first task and verify agent output in the workspace

## Fast Start Checklist

1. clone the repository and install Python and Node.js dependencies
2. install Playwright browsers and Qdrant vector store
3. set API keys in `config.toml` for at least one LLM provider
4. start the backend and frontend servers, then submit a hello-world task

## Source References

- [Devika README - Getting Started](https://github.com/stitionai/devika#getting-started)
- [Devika Installation](https://github.com/stitionai/devika#installation)
- [Devika Configuration](https://github.com/stitionai/devika#configuration)
- [Devika Repository](https://github.com/stitionai/devika)

## Summary

You now have a working Devika installation and have executed your first autonomous software engineering task from prompt to generated code.

Next: [Chapter 2: Architecture and Agent Pipeline](02-architecture-and-agent-pipeline.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 1: Getting Started**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. The Devika stack has three runtime layers: a Python FastAPI backend, a Svelte/Vite frontend, and a Qdrant vector store that persists agent memory across sessions.
2. The backend entry point is `devika.py` which starts the FastAPI server; the frontend communicates with it over a REST API on port 1337 by default.
3. On first launch, Devika initializes the SQLite database for project and session metadata and connects to the Qdrant instance (local or remote) for semantic memory.
4. Every LLM provider is configured through `config.toml`; the active model is selected per-project at task submission time.
5. Playwright is invoked by the browser agent sub-process; it requires Chromium to be installed via `playwright install`.
6. The workspace directory (`/home/user/projects` by default) is where all generated files, git repos, and project artifacts are written.
7. API key security depends entirely on `config.toml` permissions; the file must never be committed to version control.
8. The startup sequence is: Qdrant → FastAPI backend → Vite dev server; all three must be healthy before task submission.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| LLM provider | Claude 3 Haiku for low cost | Claude 3 Opus or GPT-4 for max quality | cost vs output quality |
| Qdrant mode | local in-memory Qdrant | hosted Qdrant Cloud with persistent storage | simplicity vs durability |
| Workspace storage | local filesystem | mounted network volume or S3 bucket | portability vs operational overhead |
| Frontend access | localhost only | reverse proxy with auth | dev convenience vs exposure risk |
| Python env management | system Python + pip | pyenv + virtualenv + requirements.txt pin | speed vs reproducibility |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Backend fails to start | port 1337 connection refused | missing Python dependency or wrong Python version | run `pip install -r requirements.txt` and check Python >=3.10 |
| Playwright browser missing | `BrowserType.launch: Executable doesn't exist` | `playwright install` not run | run `playwright install chromium` explicitly |
| Qdrant not reachable | `Connection refused` on vector store calls | Qdrant not started or wrong port in config | start Qdrant Docker container or set correct host in config.toml |
| API key invalid | `AuthenticationError` from LLM provider | wrong key or stale key in config.toml | verify key in provider dashboard and re-paste into config.toml |
| Frontend can't reach backend | API calls return CORS errors | frontend and backend on mismatched ports | ensure VITE_API_BASE_URL matches actual backend port |
| config.toml not found | `FileNotFoundError` on startup | missing config.toml or wrong working directory | copy `config.example.toml` to `config.toml` before first run |

### Implementation Runbook

1. Clone the repository: `git clone https://github.com/stitionai/devika.git && cd devika`.
2. Create a Python virtual environment: `python -m venv venv && source venv/bin/activate`.
3. Install Python dependencies: `pip install -r requirements.txt`.
4. Install Node.js dependencies for the frontend: `cd ui && npm install && cd ..`.
5. Install Playwright browsers: `playwright install chromium`.
6. Copy the example config: `cp config.example.toml config.toml` and fill in at least one API key.
7. Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant` or configure a remote Qdrant URL in config.toml.
8. Start the backend: `python devika.py` (confirm the API server is listening on port 1337).
9. Start the frontend: `cd ui && npm run dev` and open `http://localhost:3000` in a browser; create a project and submit a first task.

### Quality Gate Checklist

- [ ] Python version is 3.10 or higher and the virtualenv is activated
- [ ] all `pip install -r requirements.txt` packages resolve without errors
- [ ] Playwright Chromium browser is installed and `playwright install` exits cleanly
- [ ] Qdrant is reachable on the configured port before backend start
- [ ] `config.toml` contains at least one valid API key and is not committed to git
- [ ] backend `python devika.py` starts without tracebacks and logs "Uvicorn running"
- [ ] frontend dev server compiles without errors and the UI loads at localhost:3000
- [ ] first task submission returns agent output in the workspace within expected time

### Source Alignment

- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Getting Started](https://github.com/stitionai/devika#getting-started)
- [Devika Installation Section](https://github.com/stitionai/devika#installation)
- [Devika Configuration Section](https://github.com/stitionai/devika#configuration)
- [Devika Repository Root](https://github.com/stitionai/devika)

### Cross-Tutorial Connection Map

- [OpenHands Tutorial](../openhands-tutorial/) — comparable autonomous coding agent with Docker-based setup
- [SWE-agent Tutorial](../swe-agent-tutorial/) — alternative CLI-driven autonomous agent
- [Aider Tutorial](../aider-tutorial/) — simpler AI coding assistant for quick comparisons
- [Cline Tutorial](../cline-tutorial/) — VS Code extension approach to AI coding
- [Ollama Tutorial](../ollama-tutorial/) — required for local LLM backend with Devika

### Advanced Practice Exercises

1. Install Devika from scratch in a fresh Docker container and document every step that diverges from the README.
2. Configure two different LLM providers in `config.toml` and measure cold-start time for each on the same task.
3. Set up Qdrant Cloud as a remote vector store and verify that agent memory persists across server restarts.
4. Write a systemd service file or Docker Compose definition that starts the backend, frontend, and Qdrant together.
5. Submit a task that generates a multi-file Python project and inspect the workspace directory structure produced by the agents.

### Review Questions

1. What is the minimum set of services that must be running before Devika can accept a task?
2. Where does Devika write generated files, and how is the workspace path configured?
3. What happens if `playwright install` is skipped before the first task that requires web research?
4. Why should `config.toml` never be committed to git, and how do you prevent it?
5. How do you verify that the Qdrant vector store is healthy before submitting the first task?

### Scenario Playbook 1: Fresh Install on macOS

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: developer clones Devika for the first time on macOS with Homebrew Python
- initial hypothesis: Homebrew Python may conflict with virtualenv path resolution
- immediate action: verify `python3 --version` returns >=3.10 before creating the virtualenv
- engineering control: use `python3 -m venv venv` explicitly and activate before any pip commands
- verification target: `pip list` inside venv shows all requirements installed without version conflicts
- rollback trigger: any import error in `python devika.py` startup traceback
- communication step: document the exact Python version and venv activation command in team setup notes
- learning capture: add macOS-specific install notes to the project wiki and pin the Python version in CI

### Scenario Playbook 2: Qdrant Docker Not Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: backend starts but every task submission fails immediately with a connection error
- initial hypothesis: Qdrant container is not running or is using the wrong port
- immediate action: run `docker ps` to check if the Qdrant container is active
- engineering control: add a startup health check script that pings Qdrant on port 6333 before launching the backend
- verification target: backend logs show successful Qdrant connection on startup
- rollback trigger: health check fails after 10 seconds of waiting
- communication step: update the README with a clear "start Qdrant first" step order note
- learning capture: encode the Qdrant startup check into the Docker Compose `depends_on` condition

### Scenario Playbook 3: Invalid API Key at Task Submission

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task is submitted but the agent immediately reports an authentication error
- initial hypothesis: the API key in config.toml is either wrong, expired, or for the wrong organization
- immediate action: copy the key directly from the provider dashboard and paste into config.toml, then restart the backend
- engineering control: add a startup validator that tests LLM provider connectivity with a minimal ping request
- verification target: backend startup log shows "LLM provider authenticated" before accepting task requests
- rollback trigger: authentication error persists after key replacement
- communication step: check provider dashboard for key status, quota limits, and billing validity
- learning capture: document key rotation procedure and add config.toml validation to the pre-launch checklist

### Scenario Playbook 4: Frontend Cannot Reach Backend

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: UI loads but all task submissions return network errors in the browser console
- initial hypothesis: VITE_API_BASE_URL environment variable is set to a different port than the backend
- immediate action: check `ui/.env` or `ui/vite.config.js` for the API base URL and compare with the actual backend port
- engineering control: standardize backend port to 1337 and frontend proxy setting to match; document in .env.example
- verification target: browser network tab shows successful POST to `/api/execute-agent` with 200 response
- rollback trigger: CORS errors persist after port correction
- communication step: add port configuration to the onboarding checklist for new contributors
- learning capture: create a single `.env` file at the repo root that sources both backend and frontend port settings

### Scenario Playbook 5: Playwright Browser Crash on Task

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: research-heavy task fails mid-run with a Playwright executable not found error
- initial hypothesis: Playwright was installed in a different virtualenv or system Python than the one running the backend
- immediate action: activate the correct virtualenv and run `playwright install chromium` inside it
- engineering control: add `playwright install chromium` as a post-install step in the project Makefile or setup script
- verification target: `playwright --version` resolves without error inside the active virtualenv
- rollback trigger: Playwright crashes even after reinstall; check for sandboxing issues in CI or Docker environments
- communication step: update the CI pipeline YAML to include `playwright install chromium` as a named setup step
- learning capture: add explicit Playwright version pinning in requirements.txt to prevent future environment drift

### What Problem Does This Solve?

Devika's installation complexity stems from having three distinct runtimes (Python backend, Node.js frontend, Qdrant vector store) that must all be healthy simultaneously before the agent pipeline can function. Without a structured setup sequence, engineers frequently encounter cascading failures where one missing dependency causes misleading errors in a different layer. This chapter establishes the correct startup order, dependency inventory, and verification checkpoints so that every team member reaches a working baseline without guesswork.

### How it Works Under the Hood

1. The Python backend reads `config.toml` on startup and initializes provider clients for every API key present.
2. FastAPI registers all agent API endpoints and starts Uvicorn on port 1337.
3. The Qdrant client connects to the configured vector store URL and verifies the collection schema for agent memory.
4. The SQLite database is initialized (or reopened) for project, session, and task metadata storage.
5. When the frontend submits a task, FastAPI dispatches it to the agent orchestrator which spawns the multi-agent pipeline.
6. Generated files are written to the workspace path defined in config.toml under the project name subdirectory.

### Source Walkthrough

- [Devika README Getting Started](https://github.com/stitionai/devika#getting-started) — Why it matters: the canonical install sequence that defines the correct dependency order.
- [Devika config.example.toml](https://github.com/stitionai/devika/blob/main/config.example.toml) — Why it matters: the authoritative reference for all configuration keys and their default values.
- [Devika requirements.txt](https://github.com/stitionai/devika/blob/main/requirements.txt) — Why it matters: the pinned Python dependency list that determines runtime compatibility.
- [Devika devika.py](https://github.com/stitionai/devika/blob/main/devika.py) — Why it matters: the backend entry point that wires all services together on startup.

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Architecture and Agent Pipeline](02-architecture-and-agent-pipeline.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 1: Getting Started

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
