---
layout: default
title: "Chapter 6: Project Management and Workspaces"
nav_order: 6
parent: Devika Tutorial
---

# Chapter 6: Project Management and Workspaces

Welcome to **Chapter 6: Project Management and Workspaces**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter explains how Devika organizes projects, manages the workspace file system, integrates with git, and enables teams to structure and review autonomous coding sessions.

## Learning Goals

- understand the Devika project model: how projects are created, named, and isolated in the workspace
- trace how generated files are written, updated, and organized within a project workspace
- configure and use Devika's git integration for committing and reviewing agent-generated code
- manage multiple concurrent projects and maintain workspace hygiene over time

## Fast Start Checklist

1. create a new project in the Devika UI and observe the workspace directory created on disk
2. submit a task and verify generated files appear under the correct project subdirectory
3. initialize git in the project workspace and review the first commit of agent-generated code
4. explore the project list API and SQLite database to understand project metadata storage

## Source References

- [Devika Project Management Source](https://github.com/stitionai/devika/tree/main/src/project)
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika Repository](https://github.com/stitionai/devika)

## Summary

You now know how to create and manage Devika projects, navigate the workspace file structure, and use git to review, version, and share agent-generated code safely.

Next: [Chapter 7: Debugging and Troubleshooting](07-debugging-and-troubleshooting.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 6: Project Management and Workspaces**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Each Devika project is represented by a record in the SQLite database with fields for project ID, name, creation timestamp, and the LLM model selected at creation time.
2. The workspace root directory is configured in `config.toml` under `WORKSPACE_PATH`; every project gets a subdirectory named after the project name.
3. Generated files from the coder agent are written to paths relative to the project's workspace subdirectory; the orchestrator resolves absolute paths before writing.
4. Devika does not automatically initialize git in project workspaces; operators must run `git init` in the project directory and commit agent-generated code manually or via a post-task hook.
5. The frontend project list view reads project records from the SQLite API; selecting a project loads its task history and workspace file tree.
6. Task history for each project is stored as a sequence of agent interaction records in SQLite, enabling replay and audit of the full agent session.
7. Multiple projects can exist concurrently; the orchestrator routes task submissions to the correct workspace by project ID, preventing cross-project file contamination.
8. Workspace cleanup (deleting old projects) must be done manually by removing the workspace subdirectory and the SQLite project record; there is no built-in project deletion UI in early versions.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Workspace location | default local path in config.toml | mounted network volume for team sharing | simplicity vs collaboration |
| Git workflow | manual commit after task review | automated pre-commit hook that stages all changes | control vs speed |
| Project naming | free-form names in UI | enforce naming convention (e.g., JIRA-123-feature-name) | flexibility vs traceability |
| Multi-project concurrency | sequential task submission | parallel projects with separate Devika instances | simplicity vs throughput |
| Workspace cleanup | manual deletion | scheduled TTL-based archival script | control vs operational overhead |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Files written to wrong project directory | task output appears in sibling project folder | orchestrator uses project name instead of project ID for path resolution | enforce project ID as the workspace subdirectory name to avoid name collision |
| Workspace path not found | `FileNotFoundError` on task submission | WORKSPACE_PATH in config.toml points to a non-existent directory | validate WORKSPACE_PATH exists on startup and create it if absent |
| Git repo contains sensitive generated secrets | API keys appear in committed code | coder generated example code with hardcoded credentials | add a pre-commit hook with secret scanning (e.g., `git-secrets` or `truffleHog`) |
| SQLite database locked | task submission fails with database lock error | multiple concurrent writes to SQLite from parallel tasks | upgrade to PostgreSQL for concurrent deployments or serialize task writes |
| Project workspace disk full | task fails with `OSError: No space left` | accumulated workspace files from many projects exhaust disk | add disk usage monitoring and implement TTL-based workspace archival |
| Lost task history after SQLite corruption | project history unavailable | no SQLite backup policy | implement daily SQLite backup to a separate location |

### Implementation Runbook

1. Verify `WORKSPACE_PATH` in config.toml exists and is writable by the Devika process user.
2. Create a new project in the UI; verify the project subdirectory is created at `WORKSPACE_PATH/<project-name>/`.
3. Submit a task and verify generated files appear in the correct project subdirectory.
4. Navigate to the project workspace in a terminal and run `git init && git add . && git commit -m "Initial agent output"`.
5. Configure a `.gitignore` in the project workspace to exclude any secrets, `__pycache__`, and `.env` files before committing.
6. Add a secret scanning pre-commit hook using `git-secrets` or `detect-secrets` to the project workspace git configuration.
7. For team collaboration, configure the workspace path to point to a shared network volume and ensure all team members have write access.
8. Set up a weekly archival cron job that compresses and moves project workspaces older than 30 days to an archive directory.
9. Back up the SQLite database daily using `sqlite3 devika.db ".backup devika-backup-$(date +%Y%m%d).db"`.

### Quality Gate Checklist

- [ ] WORKSPACE_PATH is validated on startup and created automatically if absent
- [ ] each project workspace is isolated under a directory keyed by project ID (not just name)
- [ ] git is initialized in each new project workspace and a `.gitignore` is templated automatically
- [ ] secret scanning pre-commit hook is active in all project workspace git repos
- [ ] SQLite database is backed up daily and the backup is tested for restore validity
- [ ] disk usage for WORKSPACE_PATH is monitored with an alert threshold at 80% capacity
- [ ] project naming convention is documented and enforced through the UI or API validation
- [ ] workspace archival policy is documented and implemented as a scheduled job

### Source Alignment

- [Devika Project Module](https://github.com/stitionai/devika/tree/main/src/project)
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika config.example.toml](https://github.com/stitionai/devika/blob/main/config.example.toml)
- [Devika Repository](https://github.com/stitionai/devika)

### Cross-Tutorial Connection Map

- [OpenHands Tutorial](../openhands-tutorial/) — workspace and project management patterns in a comparable autonomous coding agent
- [Aider Tutorial](../aider-tutorial/) — git-native coding assistant for comparison on version control integration
- [Daytona Tutorial](../daytona-tutorial/) — managed development workspace service for standardizing Devika's workspace environments
- [Supabase Tutorial](../supabase-tutorial/) — PostgreSQL replacement for SQLite as Devika's project metadata store at scale
- [SWE-agent Tutorial](../swe-agent-tutorial/) — how SWE-agent manages workspace isolation for benchmark task sets

### Advanced Practice Exercises

1. Write a Devika project initialization script that creates the workspace directory, runs `git init`, adds a `.gitignore`, and installs `detect-secrets` as a pre-commit hook automatically.
2. Replace the SQLite database backend with PostgreSQL and verify that concurrent task submissions from multiple users work without lock errors.
3. Build a workspace explorer API endpoint that returns the file tree and git log for a given project ID in a format the frontend can render.
4. Implement a project archival script that compresses old workspace directories to a `.tar.gz`, verifies the archive, and removes the original directory.
5. Create a project template system that seeds new project workspaces with a standard `README.md`, `.gitignore`, and directory structure before the first task runs.

### Review Questions

1. Where does Devika store project metadata and task history, and what are the durability implications of this choice?
2. How is the project workspace directory path determined for a new project and what configuration option controls the root?
3. Why is it important to use project ID rather than project name as the workspace subdirectory name?
4. What steps are needed to add git version control to a Devika project workspace and what files should always be in `.gitignore`?
5. How does Devika ensure that files generated for one project are not written to another project's workspace?

### Scenario Playbook 1: Two Projects With the Same Name Collide

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: two users create projects named "api-backend" and files from both tasks appear in the same workspace directory
- initial hypothesis: workspace subdirectory is named by project name which is not guaranteed to be unique
- immediate action: inspect the project creation code to see if unique IDs or names are used for directory paths
- engineering control: modify the project module to use `project_id` (UUID) as the workspace directory name; store the human name only in SQLite
- verification target: two projects with the same name have distinct workspace directories and no file cross-contamination
- rollback trigger: UUID-based directories make manual navigation confusing; add a symlink from project name to UUID directory
- communication step: document the project naming policy and UUID directory convention in the operator guide
- learning capture: add a uniqueness constraint on project names in the SQLite schema to prevent duplicate names at the database level

### Scenario Playbook 2: Generated Code Contains Hardcoded API Key

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: code review reveals the coder agent generated example code with a hardcoded API key string
- initial hypothesis: the coder agent generated realistic-looking example code that included a placeholder that looks like a real key
- immediate action: revoke any potentially real keys, run `git-secrets --scan` on the workspace, and remove the offending commit
- engineering control: install `detect-secrets` as a pre-commit hook in all project workspaces so commits with secret patterns are blocked automatically
- verification target: `detect-secrets scan` on the full workspace returns zero findings after remediation
- rollback trigger: secret scanner produces too many false positives on example code patterns; tune the scanner's allowlist
- communication step: notify the security team of the incident and document the finding in the security log
- learning capture: add "never use real API key values in example code" to the coder agent system prompt

### Scenario Playbook 3: Workspace Disk Usage Grows Without Bound

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: server disk usage alert fires; investigation shows WORKSPACE_PATH consumes 200GB from 6 months of accumulated projects
- initial hypothesis: no archival or cleanup policy is in place; all projects accumulate indefinitely
- immediate action: identify projects older than 60 days, compress them to `.tar.gz` archives, and move them to cheaper storage
- engineering control: implement a weekly archival cron job that archives and removes projects inactive for 30 days; log all archival operations
- verification target: WORKSPACE_PATH size stays below 50GB after implementing the archival policy
- rollback trigger: archived project is needed by a user; implement a self-service restore procedure from archive
- communication step: communicate the archival policy to all Devika users with the 30-day retention window clearly stated
- learning capture: add disk usage as a monitored metric with alert at 80% and critical at 95% capacity

### Scenario Playbook 4: SQLite Database Locked During Parallel Task Submission

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: two users submit tasks simultaneously and one returns a database locked error
- initial hypothesis: SQLite's file-level locking prevents concurrent writes from two simultaneous task submissions
- immediate action: serialize task write operations using a Python asyncio lock around SQLite write calls
- engineering control: migrate from SQLite to PostgreSQL for concurrent team deployments; update the database URL in config.toml
- verification target: 10 concurrent task submissions all succeed without lock errors after serialization
- rollback trigger: asyncio lock causes task submission queuing that is unacceptably slow; increase worker count instead
- communication step: document SQLite concurrency limitations and the PostgreSQL migration path in the deployment guide
- learning capture: add a concurrency stress test to the CI suite that submits 5 simultaneous tasks and asserts zero lock errors

### Scenario Playbook 5: Task History Lost After Server Migration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: team migrates Devika to a new server but the SQLite database is not copied; all project history is lost
- initial hypothesis: SQLite database file was stored in the application directory which was not included in the migration plan
- immediate action: restore from the most recent backup; if no backup exists, document the data loss and establish a backup procedure
- engineering control: implement daily SQLite backup to an S3 bucket or shared network volume with 30-day retention
- verification target: daily backup job runs successfully and restore test confirms the backup is valid
- rollback trigger: backup job fails; alert immediately and investigate before the next day's backup window
- communication step: document the backup and restore procedure in the operations runbook and train the team on it
- learning capture: add backup job status as a monitored metric; include backup validation in the weekly operations review

### What Problem Does This Solve?

Devika's project and workspace management layer solves the isolation and traceability problem in autonomous code generation sessions. Without project isolation, code generated for different features or clients would intermingle in a single directory, making it impossible to track which code belongs to which task. The SQLite project record and per-project workspace directory provide the minimal structure needed to run multiple autonomous coding sessions concurrently while keeping their outputs separate and auditable.

### How it Works Under the Hood

1. When a user creates a project in the UI, the backend inserts a project record into SQLite with a UUID, name, and selected model.
2. The orchestrator creates a subdirectory under WORKSPACE_PATH using the project identifier when the first task is submitted.
3. All coder agent file writes are prefixed with the project workspace path before being passed to the file writer function.
4. Task invocations and agent interactions are logged as records in the SQLite task history table, keyed by project ID.
5. The frontend project view queries the backend for the project's task history and file tree, which is built by scanning the workspace directory.
6. Git operations (if configured) are run as subprocess calls within the project workspace directory.

### Source Walkthrough

- [Devika Project Module](https://github.com/stitionai/devika/tree/main/src/project) — Why it matters: the project creation, workspace initialization, and task history storage logic.
- [Devika config.example.toml](https://github.com/stitionai/devika/blob/main/config.example.toml) — Why it matters: the WORKSPACE_PATH and project configuration options.
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md) — Why it matters: the workspace and project isolation design rationale.
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md) — Why it matters: the user-facing description of project creation and workspace management.

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Web Research and Browser Integration](05-web-research-and-browser-integration.md)
- [Next Chapter: Chapter 7: Debugging and Troubleshooting](07-debugging-and-troubleshooting.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 6: Project Management and Workspaces

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
