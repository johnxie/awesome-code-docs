---
layout: default
title: "Chapter 4: Git Repository Source Imports"
nav_order: 4
parent: OpenSrc Tutorial
---

# Chapter 4: Git Repository Source Imports

OpenSrc can fetch direct git repositories when package metadata is not the right entry path.

## Supported Repo Inputs

- `github:owner/repo`
- `owner/repo` (defaults to GitHub)
- `owner/repo@tag` or `owner/repo#branch`
- `https://github.com/owner/repo`
- `gitlab:owner/repo` and other supported hosts

## Storage Layout

Repositories are organized under host/owner/repo path segments:

```text
opensrc/
  repos/
    github.com/
      vercel/
        ai/
```

## Source References

- [Repo parsing and resolution](https://github.com/vercel-labs/opensrc/blob/main/src/lib/repo.ts)
- [Git clone and path strategy](https://github.com/vercel-labs/opensrc/blob/main/src/lib/git.ts)

## Summary

You now understand how OpenSrc imports repository source directly and normalizes storage paths.

Next: [Chapter 5: AGENTS.md and sources.json Integration](05-agents-md-and-sources-json-integration.md)
