---
layout: default
title: "Chapter 8: Production Operations and Governance"
nav_order: 8
parent: Devika Tutorial
---

# Chapter 8: Production Operations and Governance

Welcome to **Chapter 8: Production Operations and Governance**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter covers team deployment strategies, security hardening, API cost governance, code review requirements for agent-generated code, and the operational runbooks needed to run Devika safely at scale.

## Learning Goals

- design a team deployment architecture for Devika that enforces access control and audit logging
- implement API cost governance controls that prevent runaway spend from autonomous agent tasks
- define code review and merge policies that are appropriate for agent-generated code
- build operational runbooks for incident response, key rotation, and capacity management

## Governance Checklist

- all LLM API keys are stored in a secrets manager, not in config.toml on disk
- agent-generated code requires human review before merging to protected branches
- API spend is tracked per project with per-day and per-task budget caps
- audit logs capture every task submission, agent invocation, and workspace file write

## Source References

- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Security Policy](https://github.com/stitionai/devika/blob/main/SECURITY.md)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika Repository](https://github.com/stitionai/devika)

## Summary

You now have a complete production governance framework for Devika covering security, cost controls, code review policies, and operational runbooks for safe team-scale autonomous coding.

Return to: [Tutorial Index](index.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 8: Production Operations and Governance**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Production Devika deployments replace the local `config.toml` API key storage with a secrets manager (AWS Secrets Manager, HashiCorp Vault, or GCP Secret Manager) and inject secrets at runtime via environment variables.
2. The FastAPI backend should be deployed behind a reverse proxy (Nginx or Caddy) with TLS termination and authentication middleware (JWT, SSO, or IP allowlist) to prevent unauthorized task submission.
3. LLM API cost governance is implemented by wrapping the `src/llm/` abstraction with a budget-tracking decorator that queries a spend ledger before each LLM call and blocks calls that would exceed the configured budget.
4. Agent-generated code in the project workspace should be staged in a review branch and require a human-approved pull request before merging to the main branch of any production repository.
5. All task submissions, agent invocations, and workspace writes must be captured in an immutable audit log (separate from application logs) stored in append-only storage for compliance and incident investigation.
6. Qdrant in production should run with authentication enabled and use a dedicated persistent volume with daily snapshots; the Qdrant API key must be stored in the secrets manager alongside LLM keys.
7. Capacity planning covers three resource axes: LLM API token throughput (controlled by provider rate limits and budget caps), Qdrant storage growth (controlled by TTL-based cleanup), and workspace disk (controlled by archival policy).
8. Incident response for autonomous agent systems requires a distinct runbook category: "autonomous action rollback" covering workspace file reversion, git branch deletion, and Qdrant collection cleanup.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Secret management | config.toml with strict file permissions | secrets manager with automatic rotation | setup simplicity vs security posture |
| API budget controls | manual spend monitoring | per-task budget cap with automatic kill switch | operational overhead vs cost protection |
| Code review policy | post-task human review | PR-based review with required approvers before any merge | friction vs safety |
| Access control | single shared login | per-user auth with role-based task submission limits | setup simplicity vs accountability |
| Audit logging | application log review | immutable append-only audit log with retention policy | cost vs compliance |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Runaway API spend | billing alert fires; spend 10x above baseline | no per-task budget cap; expensive model on long task | implement per-task token budget; alert at 80% and kill at 100% |
| Unauthorized task submission | unknown project in audit log | Devika UI exposed without authentication | add authentication middleware before frontend and backend API |
| Agent-generated code merged without review | production bug traced to unreviewed AI code | no merge protection on review branch | enforce branch protection rules requiring human approval on all AI-generated code PRs |
| LLM API key leaked in logs | key pattern appears in log aggregation search | key was logged in debug mode prompt payload | add secret scrubbing to log formatters; exclude key material from DEBUG logs |
| Qdrant data loss | tasks return empty research context after server restart | Qdrant running without persistent volume | mount a persistent volume and enable Qdrant snapshots |
| Compliance audit fails due to missing task records | auditor requests task history; records are incomplete | no immutable audit log; only application logs retained | implement append-only audit log with tamper-evident storage |

### Implementation Runbook

1. Deploy Devika with Docker Compose including the backend, frontend, and Qdrant services with named persistent volumes.
2. Configure a reverse proxy (Nginx) with TLS and an authentication middleware (e.g., Authelia or OAuth2 Proxy) in front of both the API and frontend.
3. Migrate all secrets from config.toml to a secrets manager and inject them as environment variables in the Docker Compose service definition.
4. Add a budget-tracking middleware to the `src/llm/` abstraction that records token usage per task and blocks calls exceeding the configured per-task cap.
5. Set up an immutable audit log sink (e.g., AWS CloudWatch Logs with object lock, or an append-only PostgreSQL audit table) for all task and agent events.
6. Enforce branch protection rules on all repositories that Devika writes to: require pull request review and status checks before merge.
7. Add secret scanning pre-commit hooks to all project workspaces using `detect-secrets` or `git-secrets`.
8. Configure Qdrant with API key authentication and enable nightly snapshot exports to S3 or equivalent durable storage.
9. Schedule weekly operational reviews covering API spend, task success rate, workspace disk usage, and Qdrant collection size metrics.

### Quality Gate Checklist

- [ ] all LLM API keys are stored in a secrets manager and injected at runtime; config.toml contains no production keys
- [ ] FastAPI backend is behind an authenticated reverse proxy and not directly accessible from the public internet
- [ ] per-task token budget cap is implemented and alerts fire at 80% consumption with hard stop at 100%
- [ ] all agent-generated code requires human review in a PR before merging to any protected branch
- [ ] immutable audit log captures all task submissions, agent invocations, and workspace writes with timestamps and user identifiers
- [ ] Qdrant is running with API key authentication and a persistent volume with daily snapshot exports
- [ ] secret scanning pre-commit hooks are active in all project workspaces
- [ ] incident response runbooks for autonomous action rollback are documented and tested quarterly

### Source Alignment

- [Devika Security Policy](https://github.com/stitionai/devika/blob/main/SECURITY.md)
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika config.example.toml](https://github.com/stitionai/devika/blob/main/config.example.toml)
- [Devika Repository](https://github.com/stitionai/devika)

### Cross-Tutorial Connection Map

- [OpenHands Tutorial](../openhands-tutorial/) — production governance patterns for a comparable autonomous coding agent
- [LangFuse Tutorial](../langfuse-tutorial/) — LLM observability and cost tracking applicable to Devika's API spend governance
- [SWE-agent Tutorial](../swe-agent-tutorial/) — governance and security considerations for autonomous coding agents
- [Supabase Tutorial](../supabase-tutorial/) — PostgreSQL backend that can replace Devika's SQLite for audit log durability
- [PostHog Tutorial](../posthog-tutorial/) — product analytics for tracking Devika usage patterns and task success rates

### Advanced Practice Exercises

1. Build a Docker Compose deployment for Devika that includes Nginx, Authelia, Devika backend, Devika frontend, Qdrant with persistent volume, and a Prometheus metrics exporter.
2. Implement a per-task token budget middleware in `src/llm/` that reads the budget from config.toml, tracks usage in a Redis counter, and kills the task if the budget is exceeded.
3. Create a GitHub Actions workflow that automatically opens a pull request with agent-generated code from a Devika workspace and assigns the configured reviewers.
4. Build an audit log exporter that reads the Devika SQLite task history and writes structured JSON audit records to an S3 bucket with server-side encryption.
5. Write an incident response runbook for the scenario where Devika commits malicious or security-violating code to a repository and document the full rollback procedure.

### Review Questions

1. What are the three resource axes that capacity planning must cover for a production Devika deployment?
2. Why is immutable append-only audit logging more important for autonomous coding agents than for traditional software tools?
3. What is the minimum code review policy that should be enforced before any Devika-generated code reaches a protected branch?
4. How does a per-task token budget cap prevent runaway API spend without requiring manual monitoring?
5. What incident response steps are unique to autonomous agent systems compared to traditional software incident response?

### Scenario Playbook 1: Runaway API Spend From a Long-Running Task

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: monthly billing alert fires at 3x the expected budget; investigation shows one task consumed 2M tokens
- initial hypothesis: a task with a broad prompt entered a long monologue loop with an expensive model, consuming tokens without producing useful output
- immediate action: identify the offending task in the audit log and terminate it if still running; review the generated output for value
- engineering control: implement per-task token budget middleware that hard-stops any task exceeding 100k tokens and sends an alert
- verification target: subsequent tasks on the same model and prompt type stay within 50k tokens per task
- rollback trigger: token cap is too low for legitimate large codebase tasks; increase cap selectively per project type
- communication step: notify the team of the new per-task token cap and the rationale; publish token usage data per project in the weekly ops review
- learning capture: add token usage as a first-class metric in the monitoring dashboard with per-project and per-model breakdowns

### Scenario Playbook 2: Devika API Exposed Without Authentication

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: security scan finds Devika's port 1337 accessible from the public internet without authentication
- initial hypothesis: the Docker Compose deployment exposed the backend port directly without a reverse proxy or firewall rule
- immediate action: immediately block port 1337 at the firewall and redeploy with Nginx reverse proxy and authentication middleware
- engineering control: standardize deployment with Docker Compose that places Nginx in front of the backend; bind backend to localhost only
- verification target: external port scan confirms port 1337 is not accessible; all requests require authentication via the proxy
- rollback trigger: authentication middleware blocks legitimate team members; verify user provisioning and auth configuration
- communication step: notify the security team of the exposure window, affected data, and remediation timeline
- learning capture: add a security deployment checklist that includes port exposure verification and authentication confirmation as required steps

### Scenario Playbook 3: Agent-Generated Code Merged Without Review

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: production incident traced to a bug in code that was directly committed from a Devika workspace without human review
- initial hypothesis: the engineer copied code directly from the workspace to the main branch without a pull request review step
- immediate action: revert the offending commit, restore the previous working state, and conduct a root cause analysis
- engineering control: enforce GitHub branch protection rules requiring at least one human reviewer on all PRs; add a CI status check that detects AI-generated file markers
- verification target: no direct commits to the main branch from Devika workspace paths; all changes go through PRs
- rollback trigger: PR requirement slows emergency fixes; add an emergency bypass process with mandatory post-hoc review
- communication step: communicate the code review policy to all team members; add it to the onboarding checklist
- learning capture: add the incident to the security postmortem log and include it in the quarterly security review

### Scenario Playbook 4: LLM API Key Leaked in Debug Logs

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: log aggregation system surfaces an alert with a pattern matching an Anthropic API key format in the backend debug log
- initial hypothesis: DEBUG log level is active in production and the full prompt payload (which includes the key from config.toml) is being logged
- immediate action: immediately rotate the exposed API key in the provider dashboard; lower the log level to INFO
- engineering control: add a log formatter that scrubs patterns matching known API key formats before writing log entries; verify at DEBUG level too
- verification target: grep for the new API key in all logs confirms zero occurrences after the scrubber is in place
- rollback trigger: log scrubbing introduces performance overhead on high-throughput systems; benchmark and optimize
- communication step: notify the security team of the key exposure event and the rotation; update the key inventory
- learning capture: add API key pattern scrubbing to the standard logging configuration and include it in the security baseline

### Scenario Playbook 5: Qdrant Data Loss After Server Restart

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: after a server restart, all tasks return empty research context; Qdrant dashboard shows an empty collection
- initial hypothesis: Qdrant was running with in-memory storage (default for `qdrant/qdrant` Docker without volume) and lost data on restart
- immediate action: restore from the most recent Qdrant snapshot if available; otherwise accept data loss and establish the backup procedure
- engineering control: redeploy Qdrant with a named Docker volume; enable scheduled snapshot exports to S3 via Qdrant's snapshot API
- verification target: Qdrant data persists across container restarts and is recoverable from S3 snapshot within 15 minutes
- rollback trigger: snapshot restore fails due to version incompatibility; pin the Qdrant Docker image version
- communication step: document the Qdrant persistence requirement prominently in the deployment guide with the required Docker volume configuration
- learning capture: add Qdrant snapshot success as a monitored metric; alert if nightly snapshot has not completed by 02:00 UTC

### What Problem Does This Solve?

Devika's production governance framework solves the accountability and blast-radius problem for autonomous AI coding agents operating in team environments. Without governance controls, a single misconfigured task can consume thousands of dollars in API spend, write security-violating code to a production repository, or expose sensitive project context to unauthorized users. The controls in this chapter create the human oversight checkpoints, cost guardrails, and audit trails that transform Devika from a powerful but risky autonomous tool into a responsibly operated engineering capability.

### How it Works Under the Hood

1. Secrets manager integration injects API keys as environment variables at container startup; the LLM abstraction layer reads from environment variables rather than config.toml in production mode.
2. The budget-tracking middleware intercepts every `LLM.inference()` call, queries a Redis counter for current task token usage, and raises a `BudgetExceededError` before the LLM call if the cap is reached.
3. The reverse proxy authenticates requests using JWT or session cookies before forwarding to the FastAPI backend; unauthenticated requests receive a 401 response.
4. The audit log sink receives structured event records via a Python logging handler and writes them to append-only storage; the handler is registered in the application startup sequence.
5. Qdrant snapshot exports are triggered via the Qdrant HTTP API on a cron schedule; snapshots are uploaded to S3 with server-side encryption.
6. Branch protection rules in GitHub (or GitLab) prevent direct pushes to protected branches; all Devika workspace code must go through a PR workflow with required reviewers.

### Source Walkthrough

- [Devika Security Policy](https://github.com/stitionai/devika/blob/main/SECURITY.md) — Why it matters: the official security reporting and hardening guidance for the Devika project.
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md) — Why it matters: the deployment and configuration baseline from which production hardening starts.
- [Devika LLM Abstraction](https://github.com/stitionai/devika/tree/main/src/llm) — Why it matters: the layer where budget controls and secret injection are implemented.
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md) — Why it matters: the architectural boundaries that inform where governance controls are most effective.

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Debugging and Troubleshooting](07-debugging-and-troubleshooting.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
