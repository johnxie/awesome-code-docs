# Awesome Code Docs: Current Gaps and Roadmap

This document tracks present-day structural and quality gaps in the repository.

## Current Snapshot (February 11, 2026)

| Metric | Value |
|:-------|:------|
| Tutorial directories | 91 |
| Tutorials with exactly 8 numbered chapters | 73 |
| Tutorials with 9 numbered chapters | 4 |
| Tutorials with 0 numbered chapters | 7 |
| Tutorials with partial chapter coverage (2-7) | 7 |

## Priority Gaps

### 1) Index-Only Tutorials

These tutorials currently publish roadmap-style `index.md` files without chapter pages:

- `tutorials/anthropic-skills-tutorial`
- `tutorials/claude-quickstarts-tutorial`
- `tutorials/mcp-servers-tutorial`
- `tutorials/openai-python-sdk-tutorial`
- `tutorials/openai-realtime-agents-tutorial`
- `tutorials/openai-whisper-tutorial`
- `tutorials/tiktoken-tutorial`

### 2) Partial `docs/` Tutorial Sets

These tutorials have chapter content but partial coverage in `docs/`:

- `tutorials/logseq-knowledge-management` (2 chapter docs)
- `tutorials/teable-database-platform` (3 chapter docs)
- `tutorials/athens-research-knowledge-graph` (3 chapter docs + setup)
- `tutorials/nocodb-database-platform` (4 chapter docs + setup)
- `tutorials/flowise-llm-orchestration` (5 chapter docs)
- `tutorials/dify-platform-deep-dive` (7 chapter docs + setup)
- `tutorials/obsidian-outliner-plugin` (4 chapter docs)

### 3) Mixed Legacy Structure

- `tutorials/codex-analysis-platform` contains both top-level chapter files and `docs/` chapter files.

## Recommended Execution Order

1. Stabilize navigation and link integrity in all indexes.
2. Align README files to published chapter reality (no over-promising links).
3. Normalize contributor templates and quality checklists.
4. Introduce automated validation for links and structure in CI.
5. Incrementally publish missing chapter docs for index-only and partial tutorials.

## Completion Criteria

A tutorial should be considered structurally complete when:

- It has `index.md` with only valid local links.
- It publishes a consistent chapter set for its chosen layout.
- Its README matches actually published files.
- It passes repository link and structure validation checks.
