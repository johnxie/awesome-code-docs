# Awesome Code Docs: Current Gaps and Roadmap

This document tracks structural and quality gaps that impact completeness and discoverability.

## Current Snapshot (auto-generated)

| Metric | Value |
|:-------|:------|
| Tutorial directories | 155 |
| Tutorials with exactly 8 numbered chapters | 152 |
| Tutorials with >8 numbered chapters | 3 |
| Tutorials with 0 numbered chapters | 0 |
| Tutorials with partial chapter coverage (1-7) | 0 |

## Current Priority Gaps

### 1) Chapter-Count Variance

Most tutorials follow the standard 8-chapter shape, but some tracks intentionally include additional chapters.

Top chapter-count tutorials:
- `n8n-mcp-tutorial`: 9 numbered chapter files
- `langchain-tutorial`: 9 numbered chapter files
- `ag2-tutorial`: 9 numbered chapter files
- `wshobson-agents-tutorial`: 8 numbered chapter files
- `whisper-cpp-tutorial`: 8 numbered chapter files
- `vllm-tutorial`: 8 numbered chapter files
- `vibesdk-tutorial`: 8 numbered chapter files
- `vibe-kanban-tutorial`: 8 numbered chapter files
- `vercel-ai-tutorial`: 8 numbered chapter files
- `turborepo-tutorial`: 8 numbered chapter files

### 2) Index Format Variance

Tutorial index pages use multiple historical styles. Priority is to keep all indexes:

- accurate
- up to date
- internally linked to related tutorials
- free of placeholder summaries

### 3) Discoverability Surfaces

High-impact surfaces requiring continuous maintenance:

- `README.md`
- `categories/*.md`
- `discoverability/tutorial-index.json`
- `discoverability/tutorial-directory.md`
- `llms.txt` and `llms-full.txt`

## Recommended Execution Order

1. Maintain link + structure + placeholder quality gates in CI.
2. Keep generated status/discoverability docs synchronized through scripts.
3. Prioritize formatting and snapshot refreshes on high-traffic tutorial tracks first.
4. Expand and normalize index formatting style guide usage across all tutorial families.

## Completion Criteria

A tutorial track is considered production-ready when:

- it has `index.md` with valid local links
- it has a coherent numbered chapter sequence
- its summary and snapshot language are not stale or placeholder quality
- it passes repository docs health checks
