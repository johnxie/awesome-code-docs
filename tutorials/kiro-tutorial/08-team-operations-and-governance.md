---
layout: default
title: "Chapter 8: Team Operations and Governance"
nav_order: 8
parent: Kiro Tutorial
---

# Chapter 8: Team Operations and Governance

Welcome to **Chapter 8: Team Operations and Governance**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Running Kiro at team scale requires deliberate governance around spec ownership, steering file reviews, autonomous delegation boundaries, and AWS-native identity integration. This chapter provides the operational playbook for production team deployments.

## Learning Goals

- design a team-scale Kiro configuration repository structure
- establish governance workflows for steering file and spec changes
- configure AWS IAM Autopilot and other Kiro Powers for enterprise environments
- set up shared MCP servers and hook libraries for team consistency
- define escalation and incident response procedures for autonomous agent failures

## Fast Start Checklist

1. create a shared `.kiro/` configuration repository or add governance files to your existing monorepo
2. define ownership rules for steering files (who approves security.md, project.md)
3. configure AWS IAM Autopilot if your team uses AWS services
4. establish a PR review policy for changes to `.kiro/specs/`, `.kiro/steering/`, and `.kiro/hooks/`
5. run a team onboarding session using the governance checklist

## Team Configuration Repository Structure

For large teams, maintain `.kiro/` as a shared configuration source committed to version control:

```
.kiro/
  specs/                    ← feature specs (PR review required for tasks.md changes)
    user-authentication/
      requirements.md
      design.md
      tasks.md
  steering/                 ← AI behavior rules (architect + security review required)
    00-project.md
    01-coding-style.md
    02-testing.md
    03-security.md
  hooks/                    ← automation rules (team lead review required)
    00-lint-on-save.md
    01-test-on-fail.md
  mcp.json                  ← MCP server config (security review required for new servers)
  settings.json             ← model routing and budget config (team lead approval)
  task-log.md               ← auto-updated by hooks; read-only for humans
```

## PR Review Policy for Kiro Configuration

| File/Directory | Required Reviewers | Review Criteria |
|:---------------|:-------------------|:----------------|
| `.kiro/steering/00-project.md` | architecture lead | technology decisions aligned with roadmap |
| `.kiro/steering/03-security.md` | security engineer | no security policy downgrades; OWASP coverage |
| `.kiro/specs/*/requirements.md` | product owner | EARS syntax compliance; acceptance criteria present |
| `.kiro/specs/*/design.md` | senior engineer | architecture coherence; data model correctness |
| `.kiro/specs/*/tasks.md` | tech lead | task scope bounded; order correct; no rogue tasks |
| `.kiro/hooks/` | team lead | no infinite-loop risk; conditions present; token efficiency |
| `.kiro/mcp.json` | security engineer | no hardcoded credentials; read-only scopes verified |
| `.kiro/settings.json` | engineering manager | budget limits set; routing policy documented |

## Kiro Powers: AWS IAM Autopilot

Kiro Powers are extensible capability modules that integrate Kiro with external systems. The first Power is **AWS IAM Autopilot**, which enables Kiro agents to interact with AWS IAM for automated permission analysis and remediation.

### What AWS IAM Autopilot Does

- analyzes IAM policies for over-permissioned roles and unused permissions
- generates least-privilege IAM policy recommendations based on actual CloudTrail usage
- creates GitHub PRs with suggested policy changes for human review and approval
- monitors new IAM policy changes and alerts on permission escalation patterns

### Enabling AWS IAM Autopilot

```json
// .kiro/settings.json
{
  "powers": {
    "awsIamAutopilot": {
      "enabled": true,
      "awsRegion": "us-east-1",
      "awsAccountId": "${AWS_ACCOUNT_ID}",
      "cloudtrailLogGroup": "${CLOUDTRAIL_LOG_GROUP}",
      "prRepository": "org/infrastructure",
      "alertOnEscalation": true,
      "escalationAlertChannel": "#security-alerts"
    }
  }
}
```

### IAM Autopilot Workflow

```
# In the Chat panel:
> Analyze IAM permissions for the ECS task role used by the auth service

[Agent] Querying CloudTrail logs for role: ecs-auth-service-role (last 90 days)
[Agent] Identified 12 permissions used, 31 permissions granted but never used
[Agent] Generating least-privilege policy recommendation...
[Agent] Creating PR in org/infrastructure: "iam: reduce auth-service-role to least privilege"
[Agent] PR #847 created: https://github.com/org/infrastructure/pull/847
```

### IAM Autopilot Safety Controls

| Control | Configuration | Purpose |
|:--------|:--------------|:--------|
| PR-only mode | `"mode": "pr-only"` | agent creates PRs but never applies changes directly |
| CloudTrail lookback window | `"lookbackDays": 90` | controls the analysis window for permission usage |
| Escalation alerts | `"alertOnEscalation": true` | notifies security team when new policy grants exceed baseline |
| Scope restriction | `"targetRoles": ["ecs-*", "lambda-*"]` | limits analysis to specific IAM role name patterns |

## Team Onboarding Workflow

```markdown
# Kiro Team Onboarding Checklist

## Installation (each developer)
- [ ] Download Kiro from kiro.dev for their platform
- [ ] Authenticate with the team's preferred provider (GitHub/AWS Builder ID)
- [ ] Clone the project repository and open in Kiro
- [ ] Verify the .kiro/ directory is loaded and steering files are active

## Environment Setup (each developer)
- [ ] Copy .env.example to .env and fill in MCP server credentials
- [ ] Verify each MCP server is active in Kiro settings
- [ ] Run /usage and confirm the model routing is correct
- [ ] Read all steering files in .kiro/steering/ to understand team conventions

## Spec Workflow Training (each developer)
- [ ] Read an existing completed spec (requirements.md → design.md → tasks.md)
- [ ] Create a practice spec for a small personal task
- [ ] Run one autonomous agent task and review the activity log
- [ ] Participate in one spec review PR as a reviewer

## Governance Training (tech leads and senior engineers)
- [ ] Review the PR review policy for .kiro/ changes
- [ ] Complete the security steering file review checklist
- [ ] Understand the escalation path for autonomous agent incidents
- [ ] Configure budget alerts and test the notification flow
```

## Autonomous Agent Incident Response

When an autonomous agent causes an unexpected outcome in a shared environment:

```markdown
# Kiro Autonomous Agent Incident Runbook

## Immediate Response (< 5 minutes)
1. Interrupt the agent execution (Escape or Stop Agent button)
2. Run `git status` to identify all modified files
3. Run `git stash` or `git checkout -- .` to revert unintended changes
4. Record the task description and agent activity log for investigation

## Investigation (< 30 minutes)
5. Review the agent activity log for the last 20 steps before the incident
6. Identify the specific decision point that led to the unintended outcome
7. Determine whether the root cause is: task underspecification, missing steering rule, or agent reasoning failure

## Remediation (< 2 hours)
8. Update the task description or steering file to prevent recurrence
9. Re-run the task in supervised mode to verify the fix
10. Commit the updated task/steering with a clear incident reference in the commit message

## Communication
11. Notify the team in the incident channel with: what happened, what was reverted, and what was changed
12. Add the incident to the team's Kiro incident log
13. Schedule a 15-minute retrospective if the incident involved production-adjacent changes
```

## Shared Hook Library

Establish a shared hook library that all team members use:

```
.kiro/hooks/
  00-lint-on-save.md          ← maintained by: team (any member)
  01-test-failure-analysis.md ← maintained by: quality lead
  02-spec-freshness-check.md  ← maintained by: architecture lead
  03-security-scan-on-commit.md ← maintained by: security engineer
  04-doc-update-reminder.md   ← maintained by: tech writer
```

Each hook file includes a header comment identifying its owner and last review date:

```markdown
---
event: file:save
condition: file matches "src/**/*.ts"
owner: team
last_reviewed: 2025-10-15
---

# Auto-Lint TypeScript on Save
...
```

## Source References

- [Kiro Docs: Team Setup](https://kiro.dev/docs/team)
- [Kiro Docs: Powers](https://kiro.dev/docs/powers)
- [Kiro Docs: AWS IAM Autopilot](https://kiro.dev/docs/powers/iam-autopilot)
- [Kiro Docs: Governance](https://kiro.dev/docs/governance)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now have the operational playbook for team-scale Kiro deployment: governance structure, PR review policies, AWS IAM Autopilot configuration, team onboarding workflow, and autonomous agent incident response.

---

**You have completed the Kiro Tutorial.** Return to the [Tutorial Index](index.md) to explore related tutorials.

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 8: Team Operations and Governance**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 8: Team Operations and Governance` — the `.kiro/` directory as the shared configuration contract, the PR review process as the governance gate, and AWS IAM Autopilot as the infrastructure automation layer.
2. Separate control-plane decisions (PR review policies, ownership assignments, Power configurations) from data-plane execution (agent task runs, IAM analysis, hook executions).
3. Capture input contracts: team configuration in `.kiro/`, developer workstations running Kiro, AWS account ID and CloudTrail access for IAM Autopilot.
4. Trace state transitions: individual use → team config shared → governance review established → onboarding complete → incident response tested.
5. Identify extension hooks: additional Kiro Powers as they are released, custom shared hook libraries, organization-level steering templates.
6. Map ownership boundaries: security engineer owns `mcp.json` and `security.md` reviews; architecture lead owns `project.md` and `design.md` reviews; engineering manager owns budget configuration.
7. Specify rollback paths: revert `.kiro/` configuration via git; disable Powers individually in settings; use PR-only mode for IAM Autopilot to prevent direct changes.
8. Track observability signals: PR cycle time for `.kiro/` changes, autonomous agent incident rate, IAM Autopilot PR merge rate, team onboarding completion rate.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Spec ownership | developer-owned specs | product owner sign-off on requirements.md | velocity vs alignment |
| Steering governance | any developer edits | architect + security sign-off | speed vs policy integrity |
| IAM Autopilot mode | PR-only, never direct apply | pr-only with security alert on escalation | automation vs safety |
| Onboarding approach | self-service with docs | guided session with tech lead | scale vs quality |
| Incident response | informal revert + fix | structured runbook with postmortem | effort vs learning |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| steering drift | agent behavior inconsistency across developers | no review process for steering changes | require PR review for all steering file changes |
| spec sprawl | many incomplete specs with no active tasks | specs created without commitment to execution | add a "spec status" field (draft/active/complete) and review in weekly planning |
| IAM over-automation | IAM Autopilot applies changes without approval | PR-only mode not configured | enforce `"mode": "pr-only"` before enabling IAM Autopilot |
| onboarding failure | new developers cannot get Kiro working in first session | incomplete env setup docs | add `.env.example` and a setup verification checklist to the onboarding guide |
| incident escalation | autonomous agent incident affects shared staging environment | no incident response protocol | implement the 13-step runbook before enabling autonomous mode in shared environments |
| Power scope creep | IAM Autopilot analyzes roles outside the defined scope | missing `targetRoles` configuration | always configure `targetRoles` to restrict analysis to known role patterns |

### Implementation Runbook

1. Commit the team's `.kiro/` configuration directory to the shared repository with a clear README.
2. Define the PR review policy for each `.kiro/` subdirectory and add it to the contributing guide.
3. Assign named owners for `security.md`, `project.md`, and `mcp.json` with documented approval authority.
4. Configure AWS IAM Autopilot in `settings.json` with PR-only mode and `targetRoles` restrictions.
5. Run the team onboarding checklist with the first cohort of developers and collect feedback.
6. Test the autonomous agent incident runbook with a controlled test scenario before enabling full autonomy in shared environments.
7. Establish a weekly `.kiro/` configuration review as part of the team's engineering meeting.
8. Set up a Slack or Teams channel for Kiro-related alerts from budget thresholds and IAM Autopilot escalations.
9. Schedule a quarterly Kiro governance review to assess the effectiveness of the PR policies and onboarding process.

### Quality Gate Checklist

- [ ] `.kiro/` directory is committed to version control with a README and owner assignments
- [ ] PR review policy is documented in the contributing guide for all `.kiro/` subdirectories
- [ ] named owners are assigned for security.md, project.md, and mcp.json reviews
- [ ] AWS IAM Autopilot is configured with `"mode": "pr-only"` and `targetRoles` restrictions
- [ ] team onboarding checklist is complete for all active developers
- [ ] autonomous agent incident runbook is tested with a controlled scenario
- [ ] budget alerts are configured and the notification channel is verified
- [ ] quarterly governance review is scheduled on the team engineering calendar

### Source Alignment

- [Kiro Docs: Team Setup](https://kiro.dev/docs/team)
- [Kiro Docs: Powers](https://kiro.dev/docs/powers)
- [Kiro Docs: AWS IAM Autopilot](https://kiro.dev/docs/powers/iam-autopilot)
- [Kiro Docs: Governance](https://kiro.dev/docs/governance)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

### Cross-Tutorial Connection Map

- [Claude Code Tutorial](../claude-code-tutorial/)
- [Goose Tutorial](../goose-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [HumanLayer Tutorial](../humanlayer-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Design a complete governance model for a 10-person team: ownership assignments, PR review policy, and escalation path for each `.kiro/` subdirectory.
2. Run the autonomous agent incident runbook as a tabletop exercise with the team: simulate an agent that modifies the wrong database migration and practice the recovery steps.
3. Configure AWS IAM Autopilot for a test AWS account with a narrow `targetRoles` filter and validate that it generates a PR without applying changes directly.
4. Write a team onboarding guide that covers install, auth, env setup, and first spec creation in under 45 minutes for a developer who has never used Kiro.
5. Propose and document a Kiro Powers roadmap for your team: which future Powers (beyond IAM Autopilot) would provide the highest value for your AWS-based infrastructure?

### Review Questions

1. Why should `.kiro/settings.json` and `.kiro/mcp.json` require security engineer approval in the PR review policy?
2. What is the most important safety configuration for AWS IAM Autopilot before enabling it in a production AWS account?
3. What tradeoff did you make between autonomous agent efficiency and oversight in shared staging environments?
4. How would you recover if a steering file change was merged without the required security review and the change weakened an authentication policy?
5. What must be tested before enabling full autonomous mode for a team's shared feature work environment?

### Scenario Playbook 1: Team Operations - Steering Drift

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: different developers receive inconsistent agent behavior because steering files were edited without review
- initial hypothesis: steering file changes are being merged without the required architecture and security reviews
- immediate action: audit the git log for recent steering file changes and identify any that bypassed the review policy
- engineering control: add a CODEOWNERS file that requires specific reviewers for `.kiro/steering/` changes
- verification target: the next steering file PR is blocked until the designated reviewers approve
- rollback trigger: if inconsistent agent behavior affects a production feature, revert the steering file to the last reviewed commit
- communication step: notify the team of the CODEOWNERS addition and update the contributing guide
- learning capture: add steering file governance to the team's quarterly engineering review agenda

### Scenario Playbook 2: Team Operations - IAM Autopilot Scope Creep

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: IAM Autopilot generates PRs targeting IAM roles outside the configured `targetRoles` filter
- initial hypothesis: the `targetRoles` pattern is too broad or a new role was created that matches the pattern unexpectedly
- immediate action: review the generated PRs and close any that target out-of-scope roles without merging
- engineering control: narrow the `targetRoles` pattern and add a specific exclusion list for known out-of-scope roles
- verification target: IAM Autopilot generates PRs only for roles matching the intended pattern after the config update
- rollback trigger: if scope creep continues, disable IAM Autopilot and conduct a manual configuration audit
- communication step: notify the security team of the scope creep and the config change made to remediate it
- learning capture: add a quarterly review of the `targetRoles` filter to the team's IAM governance calendar

### Scenario Playbook 3: Team Operations - Autonomous Agent Incident in Staging

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: autonomous agent modifies a shared database migration in the staging environment causing test failures for other developers
- initial hypothesis: the agent executed a task with scope that included the shared migrations directory
- immediate action: interrupt the agent, revert the migration change using git, and notify the team
- engineering control: add an explicit scope exclusion for shared migration directories in the task description template
- verification target: re-run the task with the scope exclusion and confirm no shared files are modified
- rollback trigger: if the migration was already applied to the staging database, run the down migration and restore from backup
- communication step: follow the 13-step incident runbook; notify the team in the incident channel within 5 minutes
- learning capture: add "never modify shared migration files autonomously" as a rule in the task generation guidelines

### Scenario Playbook 4: Team Operations - Onboarding Failure

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: a new developer cannot get Kiro working after 2 hours because the onboarding guide is incomplete
- initial hypothesis: the `.env.example` file is missing or the MCP server setup steps are not documented
- immediate action: pair the new developer with a senior team member to complete the setup and document each missing step
- engineering control: update the onboarding guide with the missing steps and add a setup verification checklist
- verification target: the next new developer completes onboarding independently in under 45 minutes
- rollback trigger: if the onboarding guide update does not resolve the issue, schedule a group onboarding session for the next cohort
- communication step: announce the onboarding guide update in the team channel and ask the new developer to confirm it worked
- learning capture: add onboarding guide review to the pre-release checklist for every Kiro version upgrade

### Scenario Playbook 5: Team Operations - Spec Sprawl

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: `.kiro/specs/` contains 20+ spec directories with no active task execution, indicating abandoned or stale specs
- initial hypothesis: specs are being created as planning artifacts but never reaching the task execution phase
- immediate action: conduct a spec audit: categorize each spec as active, on-hold, or abandoned and add status labels
- engineering control: add a "spec status" field to the spec README template and require status updates in weekly planning
- verification target: after one sprint, each spec has a clear status and a responsible owner
- rollback trigger: if spec debt continues to grow, implement a spec age limit: any spec older than 30 days without task activity is automatically archived
- communication step: present the spec audit results in the next team planning session
- learning capture: add spec lifecycle management to the team's Kiro governance document

## What Problem Does This Solve?

Agentic tools that work brilliantly for individual developers often fail catastrophically at team scale. Without governance, steering files drift, specs accumulate without execution, autonomous agents operate without safety boundaries, and costs grow without visibility. Kiro's team operations model solves this by making governance artifacts first-class citizens: version-controlled, reviewer-assigned, and incident-runbook-backed.

In practical terms, this chapter helps you avoid three common failures:

- an autonomous agent modifying shared infrastructure because nobody defined the scope boundary for team environments
- security policy regressions when a well-meaning developer edits `security.md` without a security review
- AWS IAM Autopilot applying changes directly to a production account because PR-only mode was not configured before enabling the Power

After working through this chapter, you should be able to operate Kiro as a governed team tool with the same rigor applied to AI configuration artifacts that you apply to production infrastructure code.

## How it Works Under the Hood

Under the hood, `Chapter 8: Team Operations and Governance` follows a repeatable control path:

1. **Configuration sharing**: the `.kiro/` directory is committed to version control and distributed to all developer workstations via git pull.
2. **CODEOWNERS enforcement**: GitHub or GitLab CODEOWNERS rules block merges to `.kiro/` subdirectories without designated reviewer approval.
3. **Power activation**: when a Power like IAM Autopilot is enabled in `settings.json`, Kiro connects to the corresponding AWS service using the configured credentials.
4. **IAM analysis**: IAM Autopilot queries CloudTrail logs to identify permission usage patterns and generates a least-privilege policy recommendation.
5. **PR creation**: instead of applying changes, IAM Autopilot creates a PR in the configured infrastructure repository for human review.
6. **Incident response**: when an agent incident occurs, the runbook provides a structured 13-step recovery and learning process.

When debugging governance issues, trace this sequence from configuration sharing through CODEOWNERS enforcement to identify where the policy gap occurred.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Docs: Team Setup](https://kiro.dev/docs/team)
  Why it matters: the official guide for team-scale Kiro configuration and shared workspace setup.
- [Kiro Docs: Powers](https://kiro.dev/docs/powers)
  Why it matters: the primary reference for the Powers extension model and available Power configurations.
- [Kiro Docs: AWS IAM Autopilot](https://kiro.dev/docs/powers/iam-autopilot)
  Why it matters: the detailed reference for IAM Autopilot configuration, safety controls, and CloudTrail integration.
- [Kiro Docs: Governance](https://kiro.dev/docs/governance)
  Why it matters: documents Kiro's recommended governance practices for enterprise team deployments.

Suggested trace strategy:
- review the Powers docs before enabling any Power to understand the exact AWS permissions required by the Power
- test IAM Autopilot in a sandbox AWS account before enabling it in a production account to verify PR-only mode works as expected

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Multi-Model Strategy and Providers](07-multi-model-strategy-and-providers.md)
- [Tutorial Index](index.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 8: Team Operations and Governance

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
