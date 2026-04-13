---
layout: default
title: "Chapter 4: Usage Patterns: UI and GitHub Workflows"
nav_order: 4
parent: Open SWE Tutorial
---


# Chapter 4: Usage Patterns: UI and GitHub Workflows

Welcome to **Chapter 4: Usage Patterns: UI and GitHub Workflows**. In this part of **Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains the two primary interaction surfaces: UI and GitHub-driven automation.

## Learning Goals

- run tasks from the web interface
- trigger tasks through GitHub labels
- understand asynchronous run lifecycle
- monitor status through issues and PRs

## Workflow Modes

- interactive UI mode for direct supervision
- webhook/label mode for issue-driven automation
- automatic PR generation for completed work

## Source References

- [Open SWE Usage Intro](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/usage/intro.mdx)
- [Open SWE GitHub Usage Guide](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/usage/github.mdx)
- [Open SWE Demo](https://swe.langchain.com)

## Summary

You now understand how Open SWE connects user requests to async implementation workflows.

Next: [Chapter 5: Planning Control and Human-in-the-Loop](05-planning-control-and-human-in-the-loop.md)

## Source Code Walkthrough

### `agent/utils/github.py`

The `setup_git_credentials` function in [`agent/utils/github.py`](https://github.com/langchain-ai/open-swe/blob/HEAD/agent/utils/github.py) handles a key part of this chapter's functionality:

```py


def setup_git_credentials(sandbox_backend: SandboxBackendProtocol, github_token: str) -> None:
    """Write GitHub credentials to a temporary file using the sandbox write API.

    The write API sends content in the HTTP body (not via a shell command),
    so the token never appears in shell history or process listings.
    """
    sandbox_backend.write(_CRED_FILE_PATH, f"https://git:{github_token}@github.com\n")
    sandbox_backend.execute(f"chmod 600 {_CRED_FILE_PATH}")


def cleanup_git_credentials(sandbox_backend: SandboxBackendProtocol) -> None:
    """Remove the temporary credentials file."""
    sandbox_backend.execute(f"rm -f {_CRED_FILE_PATH}")


def _git_with_credentials(
    sandbox_backend: SandboxBackendProtocol,
    repo_dir: str,
    command: str,
) -> ExecuteResponse:
    """Run a git command using the temporary credential file."""
    cred_helper = shlex.quote(f"store --file={_CRED_FILE_PATH}")
    return _run_git(sandbox_backend, repo_dir, f"git -c credential.helper={cred_helper} {command}")


def git_push(
    sandbox_backend: SandboxBackendProtocol,
    repo_dir: str,
    branch: str,
    github_token: str | None = None,
```

This function is important because it defines how Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook implements the patterns covered in this chapter.

### `agent/utils/github.py`

The `cleanup_git_credentials` function in [`agent/utils/github.py`](https://github.com/langchain-ai/open-swe/blob/HEAD/agent/utils/github.py) handles a key part of this chapter's functionality:

```py


def cleanup_git_credentials(sandbox_backend: SandboxBackendProtocol) -> None:
    """Remove the temporary credentials file."""
    sandbox_backend.execute(f"rm -f {_CRED_FILE_PATH}")


def _git_with_credentials(
    sandbox_backend: SandboxBackendProtocol,
    repo_dir: str,
    command: str,
) -> ExecuteResponse:
    """Run a git command using the temporary credential file."""
    cred_helper = shlex.quote(f"store --file={_CRED_FILE_PATH}")
    return _run_git(sandbox_backend, repo_dir, f"git -c credential.helper={cred_helper} {command}")


def git_push(
    sandbox_backend: SandboxBackendProtocol,
    repo_dir: str,
    branch: str,
    github_token: str | None = None,
) -> ExecuteResponse:
    """Push the branch to origin, using a token if needed."""
    safe_branch = shlex.quote(branch)
    if not github_token:
        return _run_git(sandbox_backend, repo_dir, f"git push origin {safe_branch}")
    setup_git_credentials(sandbox_backend, github_token)
    try:
        return _git_with_credentials(sandbox_backend, repo_dir, f"push origin {safe_branch}")
    finally:
        cleanup_git_credentials(sandbox_backend)
```

This function is important because it defines how Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook implements the patterns covered in this chapter.

### `agent/utils/github.py`

The `git_push` function in [`agent/utils/github.py`](https://github.com/langchain-ai/open-swe/blob/HEAD/agent/utils/github.py) handles a key part of this chapter's functionality:

```py


def git_push(
    sandbox_backend: SandboxBackendProtocol,
    repo_dir: str,
    branch: str,
    github_token: str | None = None,
) -> ExecuteResponse:
    """Push the branch to origin, using a token if needed."""
    safe_branch = shlex.quote(branch)
    if not github_token:
        return _run_git(sandbox_backend, repo_dir, f"git push origin {safe_branch}")
    setup_git_credentials(sandbox_backend, github_token)
    try:
        return _git_with_credentials(sandbox_backend, repo_dir, f"push origin {safe_branch}")
    finally:
        cleanup_git_credentials(sandbox_backend)


def git_pull_branch(
    sandbox_backend: SandboxBackendProtocol,
    repo_dir: str,
    branch: str,
    github_token: str | None = None,
) -> ExecuteResponse:
    """Pull a specific branch from origin, using a token if needed."""
    safe_branch = shlex.quote(branch)
    if not github_token:
        return _run_git(sandbox_backend, repo_dir, f"git pull origin {safe_branch}")
    setup_git_credentials(sandbox_backend, github_token)
    try:
        return _git_with_credentials(sandbox_backend, repo_dir, f"pull origin {safe_branch}")
```

This function is important because it defines how Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook implements the patterns covered in this chapter.

### `agent/utils/github.py`

The `git_pull_branch` function in [`agent/utils/github.py`](https://github.com/langchain-ai/open-swe/blob/HEAD/agent/utils/github.py) handles a key part of this chapter's functionality:

```py


def git_pull_branch(
    sandbox_backend: SandboxBackendProtocol,
    repo_dir: str,
    branch: str,
    github_token: str | None = None,
) -> ExecuteResponse:
    """Pull a specific branch from origin, using a token if needed."""
    safe_branch = shlex.quote(branch)
    if not github_token:
        return _run_git(sandbox_backend, repo_dir, f"git pull origin {safe_branch}")
    setup_git_credentials(sandbox_backend, github_token)
    try:
        return _git_with_credentials(sandbox_backend, repo_dir, f"pull origin {safe_branch}")
    finally:
        cleanup_git_credentials(sandbox_backend)


async def create_github_pr(
    repo_owner: str,
    repo_name: str,
    github_token: str,
    title: str,
    head_branch: str,
    base_branch: str,
    body: str,
) -> tuple[str | None, int | None, bool]:
    """Create a draft GitHub pull request via the API.

    Args:
        repo_owner: Repository owner (e.g., "langchain-ai")
```

This function is important because it defines how Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[setup_git_credentials]
    B[cleanup_git_credentials]
    C[git_push]
    D[git_pull_branch]
    E[create_github_pr]
    A --> B
    B --> C
    C --> D
    D --> E
```
