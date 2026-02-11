---
layout: default
title: "Anthropic Skills Tutorial"
nav_order: 91
has_children: true
---

# Anthropic Skills Tutorial: Reusable AI Agent Capabilities

> Build and operate production-quality skills for Claude Code, Claude.ai, and the Claude API.

[![Stars](https://img.shields.io/github/stars/anthropics/skills?style=social)](https://github.com/anthropics/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Spec](https://img.shields.io/badge/Spec-agentskills.io-blue)](https://agentskills.io/specification)

## What are Anthropic Skills?

Anthropic Skills are packaged instructions and supporting files that Claude can load for specific jobs. A skill can be lightweight (one `SKILL.md`) or operationally rich (scripts, templates, and domain references).

The official `anthropics/skills` repository demonstrates real patterns used for:

- document generation workflows (DOCX, PDF, XLSX, PPTX)
- development and automation tasks
- enterprise process standardization
- reusable task-specific behavior across teams

## Core Concepts

| Concept | Why It Matters |
|:--------|:---------------|
| `SKILL.md` | Defines how and when the skill should be used |
| Frontmatter | Enables discovery, routing, and compatibility metadata |
| Body instructions | The behavioral contract Claude follows while the skill is active |
| `scripts/` | Deterministic external logic for tasks that should not be left to free-form generation |
| `references/` | Source material Claude can load on demand for better answers |
| `assets/` | Non-text files required by the workflow |

## Tutorial Structure

| Chapter | Topic | What You Will Learn |
|:--------|:------|:--------------------|
| [1. Getting Started](01-getting-started.md) | Setup | Skill anatomy, minimal valid skill, local iteration loop |
| [2. Skill Categories](02-skill-categories.md) | Taxonomy | How to choose category boundaries and avoid "mega-skills" |
| [3. Advanced Skill Design](03-advanced-skill-design.md) | Architecture | Multi-file composition with scripts, references, and assets |
| [4. Integration Platforms](04-integration-platforms.md) | Runtime | Claude Code, Claude.ai, and Claude API integration patterns |
| [5. Production Skills](05-production-skills.md) | Reliability | Deterministic outputs, guardrails, and validation pipelines |
| [6. Best Practices](06-best-practices.md) | Quality | Testing strategy, change management, and security hygiene |
| [7. Publishing and Sharing](07-publishing-sharing.md) | Distribution | Versioning, release channels, governance, and ownership |
| [8. Real-World Examples](08-real-world-examples.md) | Case Studies | End-to-end patterns you can adapt for real teams |

## Current Ecosystem Notes (February 11, 2026)

- The public reference implementation remains in `anthropics/skills`.
- The repository points to the evolving Agent Skills format specification at `agentskills.io/specification`.
- Claude Code supports plugin marketplace workflows for skill installation from published skill repositories.

## What You Will Build

By the end of this tutorial, you will be able to:

- design skills with clear invocation boundaries
- package repeatable outputs with strict templates
- integrate script-backed workflows safely
- publish versioned skills for internal or public reuse
- run regression checks to prevent prompt drift
- operate a skills catalog with ownership and lifecycle controls

## Prerequisites

- Basic markdown and YAML familiarity
- Working knowledge of Claude Code or Claude API workflows
- Git/GitHub basics for version control and sharing

## Related Tutorials

**Prerequisites:**
- [Anthropic API Tutorial](../anthropic-code-tutorial/) - Claude API fundamentals

**Complementary:**
- [MCP Python SDK Tutorial](../mcp-python-sdk-tutorial/) - Tool integration patterns
- [Claude Code Tutorial](../claude-code-tutorial/) - CLI-driven agent workflows

**Next Steps:**
- [MCP Servers Tutorial](../mcp-servers-tutorial/) - Reference server patterns for richer tool ecosystems

---

Ready to begin? Start with [Chapter 1: Getting Started](01-getting-started.md).

---

*Built with references from the official [anthropics/skills repository](https://github.com/anthropics/skills), linked support articles, and the Agent Skills specification.*
