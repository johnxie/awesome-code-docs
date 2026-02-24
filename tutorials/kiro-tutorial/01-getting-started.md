---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Kiro Tutorial
---

# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gets you from zero to a running Kiro workspace so you can move into spec-driven workflows without setup drift.

## Learning Goals

- download and install Kiro on Mac, Windows, or Linux
- authenticate using GitHub, Google, or AWS Builder ID
- open or create your first project
- understand the Kiro workspace layout and panel structure
- run your first AI-assisted interaction in the chat panel

## Fast Start Checklist

1. download Kiro from [kiro.dev](https://kiro.dev)
2. launch the installer for your platform
3. authenticate with GitHub, Google, or AWS Builder ID
4. open a local folder or clone a repository
5. open the Kiro chat panel and send a first message

## Installation Paths

| Platform | Method | Notes |
|:---------|:-------|:------|
| macOS | `.dmg` download from kiro.dev | drag to Applications, allow Gatekeeper |
| Windows | `.exe` installer from kiro.dev | run as administrator if needed |
| Linux | `.deb` or `.AppImage` from kiro.dev | mark AppImage executable before launch |

## Authentication Methods

Kiro supports three authentication providers at launch. All grant access to the same base capabilities.

| Method | Best For | Notes |
|:-------|:---------|:------|
| GitHub | developers with existing GitHub accounts | one-click OAuth flow |
| Google | teams using Google Workspace | standard OAuth redirect |
| AWS Builder ID | teams already using AWS services | connects to AWS identity layer |

```bash
# After launch, Kiro presents an authentication screen.
# No manual token setup is required for GitHub or Google.
# For AWS Builder ID, sign in at https://profile.aws.amazon.com
# and complete the device authorization flow shown in Kiro.
```

## First Project Flow

```
1. Launch Kiro
2. Select "Open Folder" or "Clone Repository"
3. For a new project: File > New Folder, then open it in Kiro
4. Kiro indexes the workspace automatically
5. Open the Chat panel (View > Kiro Chat or the sidebar icon)
6. Type: "Summarize this project structure"
```

## Workspace Layout

| Panel | Purpose |
|:------|:--------|
| Explorer | file tree with .kiro/ directory visible |
| Editor | multi-tab code editor (VS Code-compatible) |
| Chat | AI conversation panel with spec and agent controls |
| Terminal | integrated terminal for build and run commands |
| Specs | shortcut panel to requirements, design, and tasks files |

## First Interaction

```
# In the Chat panel, start simple:
> Summarize the top-level directory structure of this project.

# Kiro reads the workspace and responds with a structured overview.
# This confirms authentication and workspace indexing are working.
```

## Early Failure Triage

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| blank chat panel after login | auth token not saved | sign out and re-authenticate |
| project files not indexed | large repo or excluded paths | check .gitignore and Kiro workspace settings |
| model response not appearing | network proxy blocking Kiro endpoints | configure proxy in Kiro settings |
| AWS Builder ID flow hangs | device code expired | restart the sign-in flow in Kiro |

## Source References

- [Kiro Website](https://kiro.dev)
- [Kiro Docs: Getting Started](https://kiro.dev/docs/getting-started)
- [Kiro Docs: Authentication](https://kiro.dev/docs/authentication)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now have Kiro installed, authenticated, and connected to a project workspace.

Next: [Chapter 2: Spec-Driven Development Workflow](02-spec-driven-development-workflow.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 1: Getting Started**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 1: Getting Started` — Kiro process, auth layer, workspace indexer, and model API connection.
2. Separate control-plane decisions (auth provider choice, workspace configuration) from data-plane execution (model inference, file reads).
3. Capture input contracts: local filesystem path, user credentials, and workspace settings; output: indexed workspace and live chat session.
4. Trace state transitions: unauthenticated → authenticated → workspace open → indexed → chat ready.
5. Identify extension hooks: custom workspace settings, proxy configuration, and excluded-path policies.
6. Map ownership boundaries: individual developer owns auth tokens; team owns shared workspace config and .kiro/ directory.
7. Specify rollback paths: sign out and re-authenticate; reopen workspace to trigger re-indexing.
8. Track observability signals: auth success/failure logs, indexing completion time, first-message latency.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Auth provider | GitHub OAuth | AWS Builder ID with IAM | simplicity vs AWS identity integration |
| Workspace size | small repo under 10k files | large monorepo with exclusion rules | speed vs completeness |
| Network config | direct connection | proxy with allowlist for kiro.dev | ease vs enterprise security |
| Rollout method | individual install | managed deploy via MDM or package manager | velocity vs governance |
| Incident response | user self-service | IT helpdesk runbook + Kiro logs | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| auth token expiry | 401 on chat requests | long-idle session without refresh | re-authenticate; check session TTL settings |
| workspace index failure | empty context responses | large or excluded files | add explicit include patterns; reduce workspace scope |
| proxy interference | connection timeout on model calls | corporate firewall blocking kiro.dev | add kiro.dev to proxy allowlist |
| OS permission denial | Gatekeeper block on macOS | unsigned binary or quarantine flag | clear quarantine attribute: `xattr -d com.apple.quarantine Kiro.app` |
| stale credentials | silent auth failures | AWS Builder ID token not refreshed | trigger manual re-auth from Kiro settings |
| network latency spike | slow first-message response | CDN routing or model endpoint cold start | retry with smaller prompt; check Kiro status page |

### Implementation Runbook

1. Verify platform prerequisites: OS version meets Kiro minimum requirements.
2. Download Kiro from the official kiro.dev release page and verify the checksum.
3. Run the platform installer and complete any OS-level permission prompts.
4. Launch Kiro and select an authentication provider.
5. Complete the OAuth or device authorization flow and confirm the success screen.
6. Open a local project folder with at least one source file to confirm workspace indexing.
7. Send a test message in the Chat panel and verify a model response is returned.
8. Check the Explorer panel for the `.kiro/` directory (created automatically on first use).
9. Record the installed version and authentication provider for team onboarding documentation.

### Quality Gate Checklist

- [ ] Kiro launches without OS-level errors on the target platform
- [ ] authentication flow completes and the Chat panel shows the user identity
- [ ] workspace indexing completes within acceptable time for the repo size
- [ ] first chat message returns a model response without timeout
- [ ] `.kiro/` directory is visible in the Explorer panel
- [ ] proxy and network configuration is documented for team members
- [ ] rollback path (sign-out and re-authenticate) is verified and documented
- [ ] installed version is recorded for future upgrade planning

### Source Alignment

- [Kiro Website](https://kiro.dev)
- [Kiro Docs: Getting Started](https://kiro.dev/docs/getting-started)
- [Kiro Docs: Authentication](https://kiro.dev/docs/authentication)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

### Cross-Tutorial Connection Map

- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [OpenCode Tutorial](../opencode-tutorial/)
- [Chapter 2: Spec-Driven Development Workflow](02-spec-driven-development-workflow.md)

### Advanced Practice Exercises

1. Install Kiro on a second platform (if available) and compare the authentication flow differences.
2. Configure a large repository with `.kiro/` exclusion settings and measure indexing time before and after.
3. Simulate an auth token expiry by signing out mid-session and document the re-authentication steps.
4. Set up a proxy environment and verify Kiro model calls route correctly through it.
5. Create an onboarding runbook for a five-person team covering install, auth, and first-session steps.

### Review Questions

1. Which authentication method integrates most naturally with your team's existing identity provider?
2. What signal confirms that workspace indexing completed successfully before sending the first chat message?
3. What tradeoff did you make between workspace scope and indexing speed?
4. How would you recover if the AWS Builder ID device code expired during authentication?
5. What must be documented before scaling Kiro installation to a full engineering team?

### Scenario Playbook 1: Getting Started - Auth Flow Spike

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: authentication provider OAuth endpoint is slow or intermittently unavailable
- initial hypothesis: identify the smallest reproducible failure boundary in the auth redirect chain
- immediate action: protect developer productivity by switching to an alternative auth provider temporarily
- engineering control: document both GitHub and AWS Builder ID flows so teams can pivot without delay
- verification target: authentication completes within 30 seconds on a standard corporate network
- rollback trigger: if auth fails three consecutive times, escalate to IT for network proxy review
- communication step: notify team channel with auth status and estimated resolution time
- learning capture: add auth fallback procedure to onboarding runbook and automate network pre-check

### Scenario Playbook 2: Getting Started - Large Repo Indexing Failure

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: workspace indexing hangs or produces incomplete context for a monorepo over 50k files
- initial hypothesis: identify which file patterns or directories are causing indexer stalls
- immediate action: add exclusion rules for build artifacts, `node_modules`, and generated files in workspace settings
- engineering control: define a canonical `.kiro/` exclusion list for the monorepo and commit it to version control
- verification target: indexing completes in under two minutes for the scoped workspace
- rollback trigger: if context responses remain incomplete after exclusion rules, reduce workspace to a single module
- communication step: document the exclusion list decision in the team's Kiro setup guide
- learning capture: convert the exclusion list into a reusable workspace template for new team members

### Scenario Playbook 3: Getting Started - Proxy Interference

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: corporate proxy blocks model API calls from Kiro, resulting in silent timeouts
- initial hypothesis: identify the specific endpoint being blocked by running a direct curl test to kiro.dev
- immediate action: submit an IT ticket to allowlist kiro.dev and the underlying model API endpoints
- engineering control: configure Kiro's proxy settings with the corporate proxy URL and credentials
- verification target: first chat message returns a response within five seconds after proxy configuration
- rollback trigger: if proxy config causes other network issues, revert and use a personal hotspot for temporary access
- communication step: share proxy configuration steps with the team and add to the network setup section of onboarding docs
- learning capture: add a pre-install network check script that tests kiro.dev connectivity before the install begins

### Scenario Playbook 4: Getting Started - OS Permission Denial

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: macOS Gatekeeper blocks Kiro launch due to quarantine attribute on the downloaded binary
- initial hypothesis: confirm the quarantine attribute is present using `xattr -l Kiro.app`
- immediate action: clear the quarantine attribute with `xattr -d com.apple.quarantine Kiro.app` and relaunch
- engineering control: add a note in the install guide to clear quarantine after download on macOS
- verification target: Kiro launches without security dialogs after the quarantine clear
- rollback trigger: if Gatekeeper continues to block after clearing quarantine, escalate to IT for MDM policy review
- communication step: add the quarantine-clear step to the macOS section of the team install guide
- learning capture: investigate whether an enterprise-signed distribution eliminates this step for managed machines

### Scenario Playbook 5: Getting Started - Version Mismatch on Upgrade

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: a Kiro update breaks an existing workspace configuration or .kiro/ directory format
- initial hypothesis: compare the `.kiro/` directory schema between the old and new version release notes
- immediate action: back up the `.kiro/` directory before applying any upgrade
- engineering control: pin the Kiro version in team documentation until a new version is validated on the target repo
- verification target: all spec files and steering configurations load correctly after the upgrade
- rollback trigger: if the upgrade breaks existing specs, restore from backup and roll back to the previous version
- communication step: announce the upgrade validation status to the team before rolling out to all workstations
- learning capture: add a version pin and upgrade validation checklist to the team's Kiro governance document

## What Problem Does This Solve?

Most teams struggle with agentic IDE adoption because setup friction causes inconsistent baselines across developer machines. Kiro solves this by providing a single downloadable package with a guided authentication flow, auto-indexing workspace setup, and a visible `.kiro/` directory that anchors all AI configuration in version control from day one.

In practical terms, this chapter helps you avoid three common failures:

- inconsistent authentication states that cause intermittent model failures mid-session
- oversized workspace indexing that produces irrelevant context and slow responses
- undocumented network or OS requirements that block adoption for entire teams

After working through this chapter, you should be able to reason about Kiro's setup as a deterministic onboarding sequence with explicit checkpoints: installed, authenticated, workspace open, indexed, and chat ready.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started` follows a repeatable control path:

1. **Binary bootstrap**: Kiro launches a VS Code-based electron process and initializes the extension host.
2. **Auth token acquisition**: the selected OAuth provider issues a token that Kiro stores in the OS credential store.
3. **Workspace indexing**: Kiro scans the open folder, applies exclusion rules, and builds a local context index.
4. **Model connection**: Kiro establishes a secure connection to the model API endpoint using the stored auth token.
5. **Chat session initialization**: the Chat panel registers the workspace context and prepares the first-message prompt template.
6. **Operational telemetry**: Kiro emits anonymized usage signals for session start, indexing duration, and first-message latency.

When debugging setup failures, walk this sequence in order and confirm each stage completes before moving to the next.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Website](https://kiro.dev)
  Why it matters: the primary distribution point for all platform installers and release notes.
- [Kiro Docs: Getting Started](https://kiro.dev/docs/getting-started)
  Why it matters: official step-by-step guide for first-time setup across all supported platforms.
- [Kiro Docs: Authentication](https://kiro.dev/docs/authentication)
  Why it matters: documents each auth provider's flow, token lifecycle, and re-authentication steps.
- [Kiro Repository](https://github.com/kirodotdev/Kiro)
  Why it matters: source of truth for open-source components, release tags, and community issue tracking.

Suggested trace strategy:
- check the GitHub releases page for the latest version tag before installing
- compare the kiro.dev docs auth section against your team's identity provider to confirm compatibility before deploying widely

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Spec-Driven Development Workflow](02-spec-driven-development-workflow.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 1: Getting Started

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
