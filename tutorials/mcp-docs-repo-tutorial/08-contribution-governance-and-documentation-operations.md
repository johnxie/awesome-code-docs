---
layout: default
title: "Chapter 8: Contribution Governance and Documentation Operations"
nav_order: 8
parent: MCP Docs Repo Tutorial
---

# Chapter 8: Contribution Governance and Documentation Operations

This final chapter defines governance controls for teams maintaining internal MCP documentation around an archived upstream source — and explains where external contributions to MCP documentation should actually go.

## Learning Goals

- Route external documentation contributions to the correct active repositories
- Maintain internal docs synchronization with canonical MCP documentation
- Establish review and versioning policies for docs-derived architecture guidance
- Prevent stale archive content from overriding current specification updates

## Where Contributions Should Go

The `modelcontextprotocol/docs` repository is **read-only**. It does not accept issues or pull requests. All documentation contributions to the MCP project must target the active repositories:

```mermaid
flowchart TD
    CONTRIB[Contributor wants to improve MCP docs]
    CONTRIB --> Q1{What type of change?}

    Q1 --> PROTO[Protocol spec\nor concept update]
    Q1 --> SDK[Language SDK docs\nor examples]
    Q1 --> SITE[Website copy\nor navigation]
    Q1 --> TOOL[Inspector or\ntooling docs]

    PROTO --> MONOREPO[modelcontextprotocol/modelcontextprotocol\nOpen issue or PR against docs/ directory]
    SDK --> SDKREPO[Respective SDK repo:\npython-sdk · typescript-sdk · java-sdk]
    SITE --> MONOREPO
    TOOL --> INSPECTOR[modelcontextprotocol/inspector\nfor Inspector-specific issues]
```

## Internal Docs Governance Model

For teams building on MCP who maintain internal documentation derived from or referencing MCP sources:

### Ownership Structure

```mermaid
graph TD
    INTERNAL[Internal MCP Documentation]
    INTERNAL --> ARCH[Architecture Decision Records\nOwner: Platform team\nReview cycle: quarterly]
    INTERNAL --> GUIDE[Integration Guides\nOwner: API/integration team\nReview cycle: on SDK major release]
    INTERNAL --> ONBOARD[Onboarding Docs\nOwner: Enablement team\nReview cycle: semiannual]
    INTERNAL --> REF[Reference links to upstream\nOwner: All — flag when archived links are cited]
```

### Synchronization Policy

Internal documentation that references MCP concepts should follow a synchronization cadence:

| Trigger | Action |
|:--------|:-------|
| New MCP SDK major version | Review and update all import path references |
| Protocol specification change | Update architecture docs and concept glossary |
| New official transport (e.g., StreamableHTTP) | Update transport choice guidance |
| New client added to ecosystem matrix | Review capability targeting assumptions |
| Archive notice on any MCP repo | Flag all internal links to that repo for migration |

### Preventing Stale Content Propagation

The most common failure mode is copying content from an archived source into internal documentation without marking it as requiring verification. Mitigation practices:

1. **Link annotations**: Any link to `github.com/modelcontextprotocol/docs` in internal docs must be annotated with `[archived]` and the date last verified
2. **Deprecation lint**: Add a CI check that flags archived GitHub URLs in documentation files
3. **Canonical link policy**: Prefer links to `modelcontextprotocol.io` (live site) over GitHub source links where possible; the live site always reflects the current active state
4. **Scheduled review**: Quarterly audit of all MCP-referencing documentation against the active monorepo

```mermaid
flowchart LR
    LINT[CI: lint for archived URLs]
    LINT --> FAIL{Found archived\nlink without annotation?}
    FAIL -- Yes --> BLOCK[Block merge\nRequire annotation or migration]
    FAIL -- No --> PASS[Pass]
    PASS --> SCHEDULE[Quarterly: human review\nof all annotated archived links]
    SCHEDULE --> MIGRATE[Migrate links that\nhave active equivalents]
```

## Archived Contributing Guide (`development/contributing.mdx`)

The archived CONTRIBUTING.md and the `development/contributing.mdx` page describe the original documentation contribution process for the Mintlify site. Now that the site is migrated, this content is historical.

Key governance elements preserved in the archived contributing guide:
- Page format conventions (MDX + Mintlify component syntax)
- Frontmatter requirements (title, description)
- Image and asset naming conventions
- Review process expectations

These conventions are still useful as a baseline for teams building their own documentation infrastructure using Mintlify or similar platforms.

## Documentation Operations Checklist

For teams operating on MCP at scale:

### Initial Setup
- [ ] Identify which internal docs reference the `modelcontextprotocol/docs` archive
- [ ] Annotate every archived link with `[archived — verify against modelcontextprotocol.io]`
- [ ] Establish ownership assignments for each internal doc category
- [ ] Set up quarterly review calendar entries

### Ongoing Operations
- [ ] Monitor `modelcontextprotocol/modelcontextprotocol` releases for spec changes
- [ ] Subscribe to SDK release feeds (Python SDK, TypeScript SDK)
- [ ] Track MCP Inspector releases for tooling doc updates
- [ ] Review client ecosystem matrix every six months

### Migration Completion Criteria
- [ ] Zero unverified links to `github.com/modelcontextprotocol/docs` in internal docs
- [ ] All concept references point to active monorepo or live site
- [ ] All SDK import paths match current major version
- [ ] Transport documentation references StreamableHTTP for remote scenarios

## Governance Summary Diagram

```mermaid
graph TD
    ARCHIVED_REPO[modelcontextprotocol/docs\nArchived — read-only]
    ACTIVE_REPO[modelcontextprotocol/modelcontextprotocol\nActive — protocol + spec + docs]
    SDK_REPOS[SDK Repositories\npython-sdk · typescript-sdk · java-sdk]
    INTERNAL[Internal Team Docs]

    ARCHIVED_REPO -.->|historical reference only| INTERNAL
    ACTIVE_REPO -->|source of truth| INTERNAL
    SDK_REPOS -->|implementation guidance| INTERNAL
    INTERNAL -->|contributions| ACTIVE_REPO
    INTERNAL -->|bug reports + feature requests| SDK_REPOS
```

## Source References

- [Archived Docs Contributing Guide](https://github.com/modelcontextprotocol/docs/blob/main/CONTRIBUTING.md)
- [Active MCP Docs Location](https://github.com/modelcontextprotocol/modelcontextprotocol/tree/main/docs)
- [MCP Monorepo Contributing Guide](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/CONTRIBUTING.md)

## Summary

The archived repository accepts no contributions. All documentation improvements for MCP go to the active monorepo or the respective SDK repositories. Internally, treat archived content as a read-only historical reference with explicit annotations. Establish a synchronization policy driven by protocol and SDK releases, not by time alone. The governance checklist in this chapter gives your team a concrete starting point for managing MCP documentation across its full lifecycle.

Return to the [MCP Docs Repo Tutorial index](README.md).
