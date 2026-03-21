---
layout: default
title: "Chapter 6: Security, Auth, and Operational Constraints"
nav_order: 6
parent: Open SWE Tutorial
---


# Chapter 6: Security, Auth, and Operational Constraints

Welcome to **Chapter 6: Security, Auth, and Operational Constraints**. In this part of **Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter surfaces the critical security boundaries in Open SWE deployments.

## Learning Goals

- handle GitHub App credentials and webhook secrets safely
- constrain sandbox and API-key exposure
- manage user access restrictions in shared environments
- document secure operational defaults

## Security Priorities

- protect private keys and webhook secrets
- limit repository permissions to required scopes
- enforce authenticated access boundaries per run
- rotate keys and monitor suspicious webhook activity

## Source References

- [Open SWE Setup: Authentication](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/setup/authentication.mdx)
- [Open SWE Setup: Development](https://github.com/langchain-ai/open-swe/blob/main/apps/docs/setup/development.mdx)
- [Open SWE Security Policy](https://github.com/langchain-ai/open-swe/blob/main/SECURITY.md)

## Summary

You now have a practical security model for operating or auditing Open SWE forks.

Next: [Chapter 7: Fork Maintenance and Migration Strategy](07-fork-maintenance-and-migration-strategy.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `agent/utils/github.py`

The `git_add_all` function in [`agent/utils/github.py`](https://github.com/langchain-ai/open-swe/blob/HEAD/agent/utils/github.py) handles a key part of this chapter's functionality:

```py


def git_add_all(sandbox_backend: SandboxBackendProtocol, repo_dir: str) -> ExecuteResponse:
    """Stage all changes."""
    return _run_git(sandbox_backend, repo_dir, "git add -A")


def git_commit(
    sandbox_backend: SandboxBackendProtocol, repo_dir: str, message: str
) -> ExecuteResponse:
    """Commit staged changes with the given message."""
    safe_message = shlex.quote(message)
    return _run_git(sandbox_backend, repo_dir, f"git commit -m {safe_message}")


def git_get_remote_url(sandbox_backend: SandboxBackendProtocol, repo_dir: str) -> str | None:
    """Get the origin remote URL."""
    result = _run_git(sandbox_backend, repo_dir, "git remote get-url origin")
    if result.exit_code != 0:
        return None
    return result.output.strip()


_CRED_FILE_PATH = "/tmp/.git-credentials"


def setup_git_credentials(sandbox_backend: SandboxBackendProtocol, github_token: str) -> None:
    """Write GitHub credentials to a temporary file using the sandbox write API.

    The write API sends content in the HTTP body (not via a shell command),
    so the token never appears in shell history or process listings.
    """
```

This function is important because it defines how Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook implements the patterns covered in this chapter.

### `agent/utils/github.py`

The `git_commit` function in [`agent/utils/github.py`](https://github.com/langchain-ai/open-swe/blob/HEAD/agent/utils/github.py) handles a key part of this chapter's functionality:

```py


def git_commit(
    sandbox_backend: SandboxBackendProtocol, repo_dir: str, message: str
) -> ExecuteResponse:
    """Commit staged changes with the given message."""
    safe_message = shlex.quote(message)
    return _run_git(sandbox_backend, repo_dir, f"git commit -m {safe_message}")


def git_get_remote_url(sandbox_backend: SandboxBackendProtocol, repo_dir: str) -> str | None:
    """Get the origin remote URL."""
    result = _run_git(sandbox_backend, repo_dir, "git remote get-url origin")
    if result.exit_code != 0:
        return None
    return result.output.strip()


_CRED_FILE_PATH = "/tmp/.git-credentials"


def setup_git_credentials(sandbox_backend: SandboxBackendProtocol, github_token: str) -> None:
    """Write GitHub credentials to a temporary file using the sandbox write API.

    The write API sends content in the HTTP body (not via a shell command),
    so the token never appears in shell history or process listings.
    """
    sandbox_backend.write(_CRED_FILE_PATH, f"https://git:{github_token}@github.com\n")
    sandbox_backend.execute(f"chmod 600 {_CRED_FILE_PATH}")


def cleanup_git_credentials(sandbox_backend: SandboxBackendProtocol) -> None:
```

This function is important because it defines how Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook implements the patterns covered in this chapter.

### `agent/utils/github.py`

The `git_get_remote_url` function in [`agent/utils/github.py`](https://github.com/langchain-ai/open-swe/blob/HEAD/agent/utils/github.py) handles a key part of this chapter's functionality:

```py


def git_get_remote_url(sandbox_backend: SandboxBackendProtocol, repo_dir: str) -> str | None:
    """Get the origin remote URL."""
    result = _run_git(sandbox_backend, repo_dir, "git remote get-url origin")
    if result.exit_code != 0:
        return None
    return result.output.strip()


_CRED_FILE_PATH = "/tmp/.git-credentials"


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
```

This function is important because it defines how Open SWE Tutorial: Asynchronous Cloud Coding Agent Architecture and Migration Playbook implements the patterns covered in this chapter.

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


## How These Components Connect

```mermaid
flowchart TD
    A[git_add_all]
    B[git_commit]
    C[git_get_remote_url]
    D[setup_git_credentials]
    E[cleanup_git_credentials]
    A --> B
    B --> C
    C --> D
    D --> E
```
