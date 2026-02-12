---
layout: default
title: "Chapter 2: tmux and Worktree Architecture"
nav_order: 2
parent: Claude Squad Tutorial
---

# Chapter 2: tmux and Worktree Architecture

Claude Squad isolates each task using tmux sessions and git worktrees.

## Core Architecture

| Layer | Role |
|:------|:-----|
| tmux sessions | independent terminal execution contexts |
| git worktrees | branch-isolated code workspaces |
| TUI | centralized control and status view |

## Why It Works

- no branch/file conflicts across active tasks
- easier background execution and resumption
- clear separation between session runtime and repo state

## Source References

- [tmux session code](https://github.com/smtg-ai/claude-squad/blob/main/session/tmux/tmux.go)
- [git worktree code](https://github.com/smtg-ai/claude-squad/blob/main/session/git/worktree.go)

## Summary

You now understand the isolation model that powers Claude Squad parallelism.

Next: [Chapter 3: Session Lifecycle and Task Parallelism](03-session-lifecycle-and-task-parallelism.md)
