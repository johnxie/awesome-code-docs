---
layout: default
title: autoresearch Tutorial
nav_order: 95
has_children: true
format_version: v2
source_repo: https://github.com/karpathy/autoresearch
categories: [ai-agents, ml-research, training]
related_tutorials:
  - deer-flow-tutorial
  - agno-tutorial
  - babyagi-tutorial
last_updated: 2026-04-12
---

# autoresearch Tutorial

**The overnight ML research agent that runs ~100 GPU experiments while you sleep.**

autoresearch (https://github.com/karpathy/autoresearch) is a minimal, self-directing AI research agent built by Andrej Karpathy. It autonomously edits a PyTorch training script, commits the change, runs a fixed 5-minute training budget, measures validation bits-per-byte, and decides whether to keep or discard the experiment — all without human intervention. One sleeping cycle yields roughly 100 experiments.

| Property | Value |
|---|---|
| Stars | 70,978 |
| Language | Python |
| License | MIT |
| Primary metric | val_bpb (bits-per-byte) |
| GPU requirement | Single CUDA GPU (recommended: H100/A100) |
| Time per experiment | ~5 minutes (fixed wall-clock budget) |
| Experiments per night | ~100 |

## What You Will Learn

This tutorial takes you from zero to running your own autonomous ML research loop. By the end you will understand:

- The three-file design philosophy that makes autoresearch auditable and reproducible
- How `prepare.py` downloads the climbmix-400b dataset and trains a BPE tokenizer
- The modern GPT architecture in `train.py` — GQA, RoPE, QK-norm, Flash Attention 3, sliding window, Value Residual
- MuonAdamW: the hybrid optimizer combining Polar Express orthogonalization with AdamW
- Why a fixed wall-clock time budget (not step count) is the correct unit of comparison
- How `program.md` encodes the agent's entire research protocol as a readable text file
- How to read `results.tsv` and `analysis.ipynb` to extract signal from 100 nightly experiments
- Scaling and customizing the system for smaller GPUs, multiple GPUs, or alternative hardware

## Current Snapshot (auto-updated)

- repository: [`karpathy/autoresearch`](https://github.com/karpathy/autoresearch)
- stars: about **74.7k**

## Repository Structure

```
autoresearch/
├── prepare.py        # FIXED — data + tokenizer + eval harness
├── train.py          # MUTABLE — GPT model + MuonAdamW + training loop
├── program.md        # INSTRUCTIONS — agent protocol (the "research org code")
├── analysis.ipynb    # Jupyter notebook for exploring results.tsv
├── results.tsv       # Untracked experiment log (git-ignored)
└── pyproject.toml    # uv project manifest
```

## Prerequisites

| Requirement | Minimum | Recommended |
|---|---|---|
| GPU | Any CUDA GPU with 16 GB VRAM | H100 SXM 80 GB |
| Python | 3.10 | 3.12 |
| PyTorch | 2.9.1 | 2.9.1 (CUDA 12.8) |
| Package manager | pip | uv |
| Disk space | 50 GB | 200 GB |
| Time to first experiment | ~30 min | ~15 min |

## Tutorial Chapters

| # | Chapter | What you learn |
|---|---|---|
| 1 | [Getting Started](01-getting-started.md) | Problem statement, 3-file design, installation with uv |
| 2 | [Data Preparation and Training Environment](02-data-preparation-and-training-environment.md) | prepare.py, climbmix dataset, BPE tokenizer, best-fit dataloader |
| 3 | [GPT Architecture](03-gpt-architecture.md) | GPTConfig, GQA, RoPE, QK-norm, sliding window, Value Residual |
| 4 | [The MuonAdamW Optimizer](04-muonadamw-optimizer.md) | Polar Express, NorMuon, Muon vs AdamW dispatch, LR schedule |
| 5 | [The Training Loop and Fixed Time Budget](05-training-loop-and-fixed-time-budget.md) | Gradient accumulation, GC freeze, MFU tracking, evaluate_bpb |
| 6 | [The Agent Protocol](06-agent-protocol.md) | program.md, experiment loop, git as ledger, autonomy mandate |
| 7 | [Analyzing Results with analysis.ipynb](07-analyzing-results.md) | results.tsv schema, progress.png, best-hit analysis |
| 8 | [Customization and Scaling](08-customization-and-scaling.md) | Smaller GPUs, multi-GPU, multi-agent, notable forks |

## Quick-Start (3 commands)

```bash
# 1. Clone and install
git clone https://github.com/karpathy/autoresearch
cd autoresearch
uv sync

# 2. Prepare data (downloads climbmix, trains BPE tokenizer)
uv run prepare.py

# 3. Hand control to the agent
# (Open Claude / GPT-4o with program.md as system prompt, then say "go")
```

The agent takes over from step 3. Go to sleep. Check `results.tsv` in the morning.

## Design Philosophy

autoresearch embodies three principles that distinguish it from heavier MLOps frameworks:

**Simplicity over completeness.** Three files. No YAML config trees, no orchestration layers, no databases. Every decision is visible in plain Python or plain Markdown.

**Git as the experiment ledger.** Every attempted change is a commit. Every rejected change is a `git reset`. The full history of what the agent tried — including failures — lives in the repository with zero extra tooling.

**Comparable experiments by construction.** A fixed 5-minute wall-clock budget means every experiment is measured under identical conditions. No cherry-picking long runs. No step-count games.

---

*This tutorial was written for autoresearch as of April 2026 (70,978 stars, MIT license). The repository moves fast; always check the upstream source for the latest `train.py` and `program.md`.*
