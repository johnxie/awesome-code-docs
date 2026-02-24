# Repository Metadata Contract

This file tracks the canonical repository metadata used for organic discoverability on GitHub.

Last verified: auto-updated by workflow (`scripts/sync_repo_metadata.sh`)

## Canonical Metadata

- repository: `johnxie/awesome-code-docs`
- description: `World-class deep-dive tutorials for open-source AI agents, vibe coding tools, LLM frameworks, and production systems.`
- homepage: `https://github.com/johnxie/awesome-code-docs#-tutorial-catalog`

## Canonical Topics

- `ai-agents`
- `awesome-list`
- `awesome-lists`
- `llm`
- `ai-coding-assistant`
- `bolt-diy`
- `cline`
- `codebase-analysis`
- `developer-tools`
- `documentation`
- `langchain`
- `machine-learning`
- `mcp`
- `open-source`
- `openhands`
- `rag`
- `roo-code`
- `technical-writing`
- `tutorials`
- `vibe-coding`

## Why This Matters

GitHub topics and repository metadata directly affect:

- topic-page discovery
- repository search relevance
- click-through quality from GitHub surfaces

## Reapply Metadata

Run:

```bash
bash scripts/sync_repo_metadata.sh
```

## Verify Metadata

Run:

```bash
gh repo view johnxie/awesome-code-docs --json description,homepageUrl,repositoryTopics
```
